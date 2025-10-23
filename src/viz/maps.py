import os
from pathlib import Path
import math
import warnings
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib import patches
from loguru import logger
import requests
from ..utils.geocode import geocode_place
from .fonts import ensure_kr_font

# Avoid Unicode minus warnings
plt.rcParams['axes.unicode_minus'] = False
warnings.filterwarnings(
    "ignore",
    message=r"Font '.*' does not have a glyph for '\\u2212'",
    category=UserWarning,
)


def _placeholder_map(path: str, title: str):
    Path(os.path.dirname(path)).mkdir(parents=True, exist_ok=True)
    fig = plt.figure(figsize=(8, 4), dpi=100)
    plt.axis("off")
    plt.title(title)
    fig.savefig(path, dpi=100, bbox_inches="tight")
    plt.close(fig)


def _use_google_static_maps() -> bool:
    return (
        str(os.getenv('USE_GOOGLE_STATIC_MAPS', '0')).lower() in ('1', 'true', 'yes')
        and bool(os.getenv('GOOGLE_MAPS_API_KEY'))
    )


def _google_static_map(center: str, markers: list, zoom: int, size: tuple, out_path: str) -> bool:
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    if not api_key:
        return False
    base = "https://maps.googleapis.com/maps/api/staticmap"
    width, height = size
    params = [
        ("center", center),
        ("zoom", str(zoom)),
        ("size", f"{width}x{height}"),
        ("maptype", "roadmap"),
        ("key", api_key),
    ]
    for m in markers:
        try:
            lat = float(m['lat']); lng = float(m['lng'])
        except Exception:
            continue
        params.append(("markers", f"color:red|{lat},{lng}"))
    try:
        r = requests.get(base, params=params, timeout=15)
        if r.status_code == 200 and r.headers.get("Content-Type", "").startswith("image"):
            with open(out_path, "wb") as f:
                f.write(r.content)
            return True
        logger.warning("Google Static Maps failed (status {}), falling back: {}", r.status_code, out_path)
        return False
    except Exception as e:
        logger.warning("Google Static Maps error: {} ({}). Fallback.", str(e), out_path)
        return False


def render_competition_heatmap(company, country, extra_entities=None):
    out_dir = f"outputs/{company}_{country}"
    os.makedirs(out_dir, exist_ok=True)
    map_png = f"{out_dir}/map_{company}_{country}.png"
    heat_png = f"{out_dir}/03_competition_heatmap_{company}_{country}.png"
    ensure_kr_font()

    # Build entity list: primary company + optional rag file per country + caller-supplied entities
    entities = [company]
    if extra_entities:
        for ent in extra_entities:
            if isinstance(ent, str):
                entities.append(ent)
            elif isinstance(ent, dict) and ent.get('name'):
                entities.append(ent['name'])
    rag_file = Path(__file__).resolve().parents[3] / "data" / "rag_corpus" / "competition" / f"{country}_entities.txt"
    if rag_file.exists():
        try:
            for line in rag_file.read_text(encoding="utf-8").splitlines():
                name = line.strip()
                if name:
                    entities.append(name)
        except Exception:
            pass

    # Geocode markers
    markers = []
    for name in entities[:40]:
        loc = geocode_place(name, country)
        if loc:
            markers.append({"lat": loc[0], "lng": loc[1], "name": name})

    # Choose center/zoom
    if markers:
        center_lat = float(np.mean([m["lat"] for m in markers]))
        center_lng = float(np.mean([m["lng"] for m in markers]))
        center = f"{center_lat},{center_lng}"
    else:
        center = {"KR": "Seoul,KR", "JP": "Tokyo,JP", "US": "USA"}.get(country, country)
    zoom = 7 if country == "KR" else (5 if country in ("JP", "US") else 4)

    # Try Google Static Maps first (if enabled)
    if _use_google_static_maps():
        ok = _google_static_map(center=center, markers=markers, zoom=zoom, size=(800, 400), out_path=map_png)
        if not ok:
            logger.warning("Falling back to offline map for {}-{}", company, country)
    else:
        ok = False

    if not ok:
        # Offline-safe placeholder scatter
        rng = np.random.default_rng(abs(hash(f"{company}|{country}")) % (2**32))
        pts = rng.random((max(8, min(len(markers), 40)) or 10, 2))
        fig, ax = plt.subplots(figsize=(8, 4), dpi=100)
        ax.set_title(f"Competition Map | {company} - {country}")
        ax.add_patch(patches.Rectangle((0, 0), 1, 1, facecolor='#eef2ff'))
        ax.scatter(pts[:, 0], pts[:, 1], s=28, c="#2b8cbe", edgecolors="white", linewidths=0.4)
        ax.set_xticks([]); ax.set_yticks([])
        fig.savefig(map_png, dpi=100, bbox_inches='tight', pad_inches=0)
        plt.close(fig)

    # Heatmap placeholder
    # Build a density heatmap over the basemap with transparency so it's clearly a map
    try:
        base = mpimg.imread(map_png)
        h, w = base.shape[0], base.shape[1]

        # Helper: WebMercator conversions
        def _latlng_to_world_xy(lat, lng, zoom):
            scale = 256 * (2 ** zoom)
            x = (lng + 180.0) / 360.0 * scale
            siny = math.sin(math.radians(lat))
            y = (0.5 - math.log((1 + siny) / (1 - siny)) / (4 * math.pi)) * scale
            return x, y
        def _world_xy_to_latlng(x, y, zoom):
            scale = 256 * (2 ** zoom)
            lng = x / scale * 360.0 - 180.0
            n = math.pi * (1 - 2 * (y / scale))
            lat = math.degrees(math.atan(math.sinh(n)))
            return lat, lng

        # Compute geographic extent for imshow so overlays align with basemap
        if isinstance(center, str) and "," in center:
            c_lat, c_lng = [float(v) for v in center.split(",", 1)]
        else:
            # fallback capitals
            c_lat, c_lng = (37.5665, 126.9780) if country == "KR" else ((35.6762, 139.6503) if country == "JP" else (40.0, -95.0))
        cx, cy = _latlng_to_world_xy(c_lat, c_lng, zoom)
        left = cx - w/2; right = cx + w/2; top = cy - h/2; bottom = cy + h/2
        lat_top, lng_left = _world_xy_to_latlng(left, top, zoom)
        lat_bot, lng_right = _world_xy_to_latlng(right, bottom, zoom)

        fig2, ax2 = plt.subplots(figsize=(w/100, h/100), dpi=100)
        ax2.imshow(base, extent=[lng_left, lng_right, lat_bot, lat_top])
        ax2.set_xlim(lng_left, lng_right); ax2.set_ylim(lat_bot, lat_top)
        ax2.set_xticks([]); ax2.set_yticks([])

        # If we have real markers (lat/lng), create a density grid; else use a light vignette
        if markers:
            lngs = np.array([m['lng'] for m in markers])
            lats = np.array([m['lat'] for m in markers])
            # 2D histogram over map extent
            bins_x = 60; bins_y = 30
            H, xedges, yedges = np.histogram2d(lngs, lats, bins=[bins_x, bins_y], range=[[lng_left, lng_right], [lat_bot, lat_top]])
            # Simple Gaussian-like blur via separable kernel
            ker = np.array([1, 2, 4, 2, 1], dtype=float)
            ker = ker / ker.sum()
            # blur x
            Hx = np.apply_along_axis(lambda v: np.convolve(v, ker, mode='same'), axis=0, arr=H)
            # blur y
            Hxy = np.apply_along_axis(lambda v: np.convolve(v, ker, mode='same'), axis=1, arr=Hx)
            Hxy = Hxy.T  # align to imshow orientation
            alpha = 0.45
            ax2.imshow(
                Hxy,
                extent=[lng_left, lng_right, lat_bot, lat_top],
                origin='lower',
                cmap='YlOrRd',
                alpha=alpha,
                aspect='auto',
                interpolation='bilinear',
            )
        else:
            # subtle overlay to indicate lack of data
            ax2.add_patch(patches.Rectangle((lng_left, lat_bot), (lng_right - lng_left), (lat_top - lat_bot), facecolor='white', alpha=0.12, linewidth=0))

        ax2.set_title(f"Competition Density | {company} - {country}")
        fig2.savefig(heat_png, dpi=100, bbox_inches='tight', pad_inches=0)
        plt.close(fig2)
    except Exception:
        # Fallback: simple translucent grid as last resort
        rng_heat = np.random.default_rng(abs(hash(f"{company}|{country}|heatmap")) % (2**32))
        fig2, ax2 = plt.subplots(figsize=(8, 4), dpi=100)
        ax2.set_title(f"Competition Heatmap | {company} - {country}")
        grid = rng_heat.random((5, 10))
        ax2.imshow(grid, cmap='YlOrRd', aspect='auto', alpha=0.5)
        ax2.set_xticks([]); ax2.set_yticks([])
        fig2.savefig(heat_png, dpi=100, bbox_inches='tight')
        plt.close(fig2)

    positioning = {"axis": ["price", "service"], "point": "mid-high"}
    whitespaces = ["SE corridor", "Port-adjacent SMB", "Cross-border niche"]
    return heat_png, map_png, positioning, whitespaces


def render_partner_map(company, country, candidates):
    path = f"outputs/{company}_{country}/04_partner_map_{company}_{country}.png"
    ensure_kr_font()

    # Geocode partner names
    pts = []
    for c in candidates:
        name = c.get("name")
        loc = geocode_place(name, country)
        if loc:
            pts.append({"lat": loc[0], "lng": loc[1], "name": name})

    # Determine center/zoom
    if pts:
        center_lat = float(np.mean([p["lat"] for p in pts]))
        center_lng = float(np.mean([p["lng"] for p in pts]))
        center = f"{center_lat},{center_lng}"
    else:
        center = {"KR": "Seoul,KR", "JP": "Tokyo,JP", "US": "USA"}.get(country, country)
    zoom = 7 if country == "KR" else (5 if country in ("JP", "US") else 4)

    # Try Google Static Maps
    ok = False
    if _use_google_static_maps():
        ok = _google_static_map(center=center, markers=pts, zoom=zoom, size=(800, 400), out_path=path)

    if not ok:
        # Offline-safe scatter with labels
        rng = np.random.default_rng(abs(hash(f"partners|{company}|{country}")) % (2**32))
        n = max(3, len(candidates))
        xs, ys = rng.random(n), rng.random(n)
        fig, ax = plt.subplots(figsize=(8, 4), dpi=100)
        ax.set_title(f"Partner Map | {company} - {country}")
        ax.add_patch(patches.Rectangle((0, 0), 1, 1, facecolor='#ecfeff'))
        ax.scatter(xs, ys, s=30, c="#0891b2", edgecolors="white", linewidths=0.5)
        for i in range(min(n, 8)):
            name = (candidates[i % len(candidates)].get('name') if candidates else f'p{i+1}') or f'p{i+1}'
            ax.text(xs[i], ys[i], name[:12], color="#0e7490", fontsize=9, ha='center', va='center')
        ax.set_xticks([]); ax.set_yticks([])
        fig.savefig(path, dpi=100, bbox_inches='tight', pad_inches=0)
        plt.close(fig)
    return path
