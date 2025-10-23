import os
import os as _os
import matplotlib.pyplot as plt
import warnings
import requests
from pathlib import Path
from ..utils.geocode import geocode_place
from loguru import logger
from .fonts import ensure_kr_font

# Avoid Unicode minus warnings globally in this module
plt.rcParams['axes.unicode_minus'] = False
warnings.filterwarnings(
    "ignore",
    message=r"Font '.*' does not have a glyph for '\\u2212'",
    category=UserWarning,
)
import numpy as np
import math
import matplotlib.image as mpimg
from matplotlib import patches


def _google_static_map(center: str, markers: list, zoom: int, size: tuple, out_path: str) -> bool:
    api_key = _os.getenv("GOOGLE_MAPS_API_KEY")
    if not api_key:
        logger.warning("GOOGLE_MAPS_API_KEY not set. Falling back to stub image for {}", out_path)
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
    # Add markers
    for m in markers:
        params.append(("markers", f"color:red|{m['lat']},{m['lng']}"))
    try:
        r = requests.get(base, params=params, timeout=15)
        if r.status_code == 200 and r.headers.get("Content-Type", "").startswith("image"):
            with open(out_path, "wb") as f:
                f.write(r.content)
            return True
        logger.warning(
            "Google Static Maps request failed (status: {status}). Using fallback for {path}",
            status=r.status_code,
            path=out_path,
        )
        return False
    except Exception as e:
        logger.warning("Google Static Maps request error: {}. Using fallback for {}", str(e), out_path)
        return False


def render_competition_heatmap(company, country, extra_entities=None):
    out_dir = f"outputs/{company}_{country}"
    os.makedirs(out_dir, exist_ok=True)
    map_png = f"{out_dir}/map_{company}_{country}.png"
    heat_png = f"{out_dir}/03_competition_heatmap_{company}_{country}.png"
    ensure_kr_font()

    # Build entity list: primary company + optional rag file per country + caller-supplied entities
    # extra_entities can be a list of names or dicts {name, category, homepage}
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

    # Geocode to markers and attach category if known
    markers = []
    cat_lookup = {}
    if isinstance(extra_entities, list):
        for ent in extra_entities:
            if isinstance(ent, dict) and ent.get('name'):
                cat_lookup[ent['name']] = ent.get('category','')
    for name in entities[:40]:
        loc = geocode_place(name, country)
        if loc:
            markers.append({
                "lat": loc[0],
                "lng": loc[1],
                "name": name,
                "category": cat_lookup.get(name,''),
                "source": "geocode"
            })

    # Fallback markers if nothing geocoded
    if not markers:
        anchors = {
            "KR": [(37.5665, 126.9780), (35.1796, 129.0756)],
            "JP": [(35.6762, 139.6503), (34.6937, 135.5023)],
        }.get(country, [(0.0, 0.0)])
        rng = np.random.default_rng(42)
        for i, (lat, lng) in enumerate(anchors):
            markers.append({
                "lat": lat + float(rng.normal(0, 0.05)),
                "lng": lng + float(rng.normal(0, 0.05)),
                "name": f"anchor_{i+1}",
                "source": "fallback",
            })

    # Determine map center: mean of marker coords if available, otherwise capital city fallback
    if markers:
        center_lat = float(np.mean([m["lat"] for m in markers]))
        center_lng = float(np.mean([m["lng"] for m in markers]))
        center = f"{center_lat},{center_lng}"
    else:
        center = {
            "KR": "Seoul,KR",
            "JP": "Tokyo,JP",
        }.get(country, country)

    # Choose zoom dynamically (KR more zoomed-in)
    def _estimate_zoom(markers_list):
        if not markers_list:
            return 8 if country == "KR" else 6
        lats = np.array([m["lat"] for m in markers_list])
        lngs = np.array([m["lng"] for m in markers_list])
        span = max(lngs.max() - lngs.min(), lats.max() - lats.min())
        span = max(span, 0.5)
        base = math.log2(360.0 / (span * 1.5))
        z = int(max(6, min(10, round(base))))
        if country == "KR":
            z = max(z, 8)
        return z

    zoom = _estimate_zoom(markers)

    # Fetch a clean base map (no markers) we can overlay on
    ok = _google_static_map(center=center, markers=[], zoom=zoom, size=(800, 400), out_path=map_png)
    if not ok:
        # Create a blank white base of expected size if Google map not available
        fig = plt.figure(figsize=(8, 4), dpi=100)
        plt.axis("off")
        fig.savefig(map_png, dpi=100, bbox_inches="tight")
        plt.close(fig)

    # Build overlay heatmap on top of the base map image
    try:
        base_img = mpimg.imread(map_png)
        h, w = base_img.shape[0], base_img.shape[1]

        # Compute geographic extent of the static map image using Web Mercator
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

        # Use same zoom value used for base map
        if isinstance(center, str) and "," in center:
            c_lat, c_lng = [float(v) for v in center.split(",", 1)]
        else:
            # Fallback center by country capital
            c_lat, c_lng = (37.5665, 126.9780) if country == "KR" else (35.6762, 139.6503)

        cx, cy = _latlng_to_world_xy(c_lat, c_lng, zoom)
        # Image spans w x h pixels around center
        left = cx - w / 2
        right = cx + w / 2
        top = cy - h / 2
        bottom = cy + h / 2
        lat_top, lng_left = _world_xy_to_latlng(left, top, zoom)
        lat_bot, lng_right = _world_xy_to_latlng(right, bottom, zoom)

        # Plot background and overlay density
        fig, ax = plt.subplots(figsize=(w / 100, h / 100), dpi=100)
        ax.imshow(base_img, extent=[lng_left, lng_right, lat_bot, lat_top], zorder=0)
        # Slightly dim the base map to boost heat visibility
        ax.add_patch(
            patches.Rectangle((lng_left, lat_bot), (lng_right - lng_left), (lat_top - lat_bot),
                               facecolor='white', alpha=0.25, linewidth=0, zorder=1)
        )
        if markers:
            lats = np.array([m["lat"] for m in markers])
            lngs = np.array([m["lng"] for m in markers])
            hb = ax.hexbin(lngs, lats, gridsize=24, cmap="Reds", alpha=0.85, mincnt=1, bins='log', zorder=2)
            # Colorize scatter by category
            size_default = int(os.getenv('MARKER_SIZE_DEFAULT', '24'))
            size_kr = int(os.getenv('MARKER_SIZE_KR', '36'))
            s = size_kr if country == 'KR' else size_default
            palette = {
                'CEP': '#1f77b4',
                '3PL/CEP': '#2ca02c',
                'Postal/CEP': '#9467bd',
                'E-commerce Fulfillment': '#ff7f0e',
                'Marketplace Fulfillment': '#d62728',
            }
            colors = []
            for m in markers:
                c = palette.get(m.get('category',''), '#b10026')
                colors.append(c)
            ax.scatter(lngs, lats, s=s, c=colors, edgecolors="white", linewidths=0.5, zorder=3)
            # Legend
            try:
                import matplotlib.patches as mpatches
                patches_list = []
                used = {}
                for m in markers:
                    lab = m.get('category','') or 'Other'
                    if lab in used:
                        continue
                    used[lab] = True
                    col = palette.get(m.get('category',''), '#b10026')
                    patches_list.append(mpatches.Patch(color=col, label=lab))
                if patches_list:
                    ax.legend(handles=patches_list, loc='lower left', fontsize=7, framealpha=0.7)
            except Exception:
                pass
            try:
                cbar = fig.colorbar(hb, ax=ax, fraction=0.035, pad=0.012)
                cbar.ax.tick_params(labelsize=7)
            except Exception:
                pass
        ax.set_xlim(lng_left, lng_right)
        ax.set_ylim(lat_bot, lat_top)
        ax.set_xticks([]); ax.set_yticks([])
        fig.savefig(heat_png, dpi=100, bbox_inches="tight", pad_inches=0)
        plt.close(fig)
    except Exception as e:
        logger.warning("Failed to build overlay heatmap: {}", str(e))
        # Fallback to simple density figure
        if markers:
            lats = np.array([m["lat"] for m in markers])
            lngs = np.array([m["lng"] for m in markers])
            plt.figure(figsize=(6, 3))
            hb = plt.hexbin(lngs, lats, gridsize=24, cmap="Reds", mincnt=1, bins='log')
            plt.xticks([]); plt.yticks([])
            plt.savefig(heat_png, dpi=150, bbox_inches="tight")
            plt.close()
        else:
            plt.figure(figsize=(6, 3))
            plt.text(0.5, 0.5, "No points", ha="center", va="center")
            plt.axis("off")
            plt.savefig(heat_png, dpi=150, bbox_inches="tight")
            plt.close()

    # Optionally save debug CSV; basemap is now always kept because report requires map_*.png
    debug = str(os.getenv('DEBUG_ARTIFACTS', '0')).lower() in ('1','true','yes')
    try:
        if debug:
            import csv
            ev_dir = Path(__file__).resolve().parents[3]/'artifacts'/'evidence'/f"{company}_{country}"
            ev_dir.mkdir(parents=True, exist_ok=True)
            csv_path = ev_dir / f"competition_points_{company}_{country}.csv"
            with open(csv_path, 'w', newline='', encoding='utf-8') as cf:
                w = csv.writer(cf); w.writerow(["name","lat","lng","source"])
                for m in markers:
                    w.writerow([m.get('name',''), m['lat'], m['lng'], m.get('source','')])
            logger.info("Competition points written: {}", str(csv_path))
    except Exception:
        pass

    # Always return basemap path for report references
    markers_map_png = map_png

    positioning = {"axis": ["price", "service"], "point": "mid-high"}
    whitespaces = ["SE corridor", "Port-adjacent SMB", "Cross-border niche"]
    return heat_png, markers_map_png, positioning, whitespaces


def render_partner_map(company, country, candidates):
    os.makedirs(f"outputs/{company}_{country}", exist_ok=True)
    path = f"outputs/{company}_{country}/04_partner_map_{company}_{country}.png"
    ensure_kr_font()

    # Geocode partner names
    pts = []
    for c in candidates:
        name = c.get("name")
        loc = geocode_place(name, country)
        if loc:
            pts.append({"lat": loc[0], "lng": loc[1], "role": c.get("role", ""), "name": name})

    # Determine center
    if pts:
        center_lat = float(np.mean([p["lat"] for p in pts]))
        center_lng = float(np.mean([p["lng"] for p in pts]))
        center = f"{center_lat},{center_lng}"
    else:
        center = {"KR": "Seoul,KR", "JP": "Tokyo,JP"}.get(country, country)

    # Base map (no markers); we overlay our own points for consistent style
    zoom = 7 if country == "KR" else 5
    ok = _google_static_map(center=center, markers=[], zoom=zoom, size=(800, 400), out_path=path)
    if not ok:
        fig = plt.figure(figsize=(8, 4), dpi=100)
        plt.axis("off")
        fig.savefig(path, dpi=100, bbox_inches="tight")
        plt.close(fig)

    try:
        base = mpimg.imread(path)
        h, w = base.shape[0], base.shape[1]
        # Compute geographic extent for proper overlay
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
        if isinstance(center, str) and "," in center:
            c_lat, c_lng = [float(v) for v in center.split(",", 1)]
        else:
            c_lat, c_lng = (37.5665, 126.9780) if country == "KR" else (35.6762, 139.6503)
        cx, cy = _latlng_to_world_xy(c_lat, c_lng, zoom)
        left = cx - w/2; right = cx + w/2; top = cy - h/2; bottom = cy + h/2
        lat_top, lng_left = _world_xy_to_latlng(left, top, zoom)
        lat_bot, lng_right = _world_xy_to_latlng(right, bottom, zoom)

        fig, ax = plt.subplots(figsize=(w/100, h/100), dpi=100)
        ax.imshow(base, extent=[lng_left, lng_right, lat_bot, lat_top])
        ax.add_patch(patches.Rectangle((lng_left, lat_bot), (lng_right - lng_left), (lat_top - lat_bot), facecolor='white', alpha=0.15, linewidth=0))
        if pts:
            lats = np.array([p["lat"] for p in pts]); lngs = np.array([p["lng"] for p in pts])
            ax.scatter(lngs, lats, s=28 if country=="KR" else 20, c="#2b8cbe", edgecolors="white", linewidths=0.4)
            for p in pts[:8]:
                ax.text(p["lng"], p["lat"], "•", color="#08519c", fontsize=10, ha='center', va='center')
        ax.set_xlim(lng_left, lng_right); ax.set_ylim(lat_bot, lat_top)
        ax.set_xticks([]); ax.set_yticks([])
        fig.savefig(path, dpi=100, bbox_inches='tight', pad_inches=0)
        plt.close(fig)
    except Exception:
        # Fallback text
        txt = "\n".join([f"{c['name']}({c['role']})" for c in candidates])
        plt.figure(figsize=(8, 4))
        plt.title(f"Partner Map {company}-{country}")
        plt.text(0.05, 0.5, txt)
        plt.axis('off')
        plt.savefig(path, dpi=150, bbox_inches='tight')
        plt.close()
    # Save debug CSV for partners (artifacts) when DEBUG_ARTIFACTS=1
    try:
        if str(os.getenv('DEBUG_ARTIFACTS','0')).lower() in ('1','true','yes'):
            import csv
            ev_dir = Path(__file__).resolve().parents[3]/'artifacts'/'evidence'/f"{company}_{country}"
            ev_dir.mkdir(parents=True, exist_ok=True)
            csv_path = ev_dir / f"partner_points_{company}_{country}.csv"
            with open(csv_path, 'w', newline='', encoding='utf-8') as cf:
                w = csv.writer(cf); w.writerow(["name","role","lat","lng","source"])
                for p in pts:
                    w.writerow([p.get('name',''), p.get('role',''), p['lat'], p['lng'], p.get('source','')])
            logger.info("Partner points written: {}", str(csv_path))
    except Exception:
        pass
    return path
