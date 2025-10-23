import os
import re
import warnings
import matplotlib.pyplot as plt
from matplotlib import patches

# Ensure ASCII minus is used to avoid U+2212 glyph warnings
plt.rcParams['axes.unicode_minus'] = False
# Also silence any remaining matplotlib warnings about missing U+2212 glyphs
warnings.filterwarnings(
    "ignore",
    message=r"Font '.*' does not have a glyph for '\\u2212'",
    category=UserWarning,
)
from .fonts import ensure_kr_font


def _set_kr_font():
    ensure_kr_font()


def _parse_numeric(value):
    """Try to parse value like 'Y%', '~$X', '123', '12.3%'. Return float or None."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    s = str(value)
    # percent
    m = re.match(r"\s*([~≃≈]?)\s*([0-9]+(?:\.[0-9]+)?)\s*%\s*", s)
    if m:
        return float(m.group(2))
    # currency like ~$123, $1.2B, 1.2B
    m = re.match(r"\s*([~≃≈]?)\s*\$?\s*([0-9]+(?:\.[0-9]+)?)\s*([KMB])?\s*", s, re.I)
    if m:
        val = float(m.group(2))
        unit = (m.group(3) or "").upper()
        mult = {"K": 1e3, "M": 1e6, "B": 1e9}.get(unit, 1.0)
        return val * mult
    # plain number
    try:
        return float(s)
    except Exception:
        return None


def render_market_summary_png(company, country, metrics):
    """Render a compact dashboard: bar chart for numeric metrics + key/value panel."""
    os.makedirs(f"outputs/{company}_{country}", exist_ok=True)
    path = f"outputs/{company}_{country}/01_market_summary_{company}_{country}.png"

    _set_kr_font()
    fig = plt.figure(figsize=(7, 3))
    fig.suptitle(f"Market Summary | {company} - {country}", fontsize=11, y=0.98)

    # Split area: left bars, right text
    gs = fig.add_gridspec(1, 2, width_ratios=[1.2, 1.8])
    ax_bar = fig.add_subplot(gs[0, 0])
    ax_txt = fig.add_subplot(gs[0, 1])

    # Prepare numeric bars
    keys = list(metrics.keys()) if isinstance(metrics, dict) else []
    vals = []
    labels = []
    for k in keys:
        v = _parse_numeric(metrics.get(k))
        if v is not None:
            labels.append(k)
            vals.append(v)
    if vals:
        ax_bar.barh(range(len(vals)), vals, color="#5B8FF9")
        ax_bar.set_yticks(range(len(vals)))
        ax_bar.set_yticklabels(labels, fontsize=9)
        ax_bar.invert_yaxis()
        ax_bar.set_xlabel("value (normalized)", fontsize=8)
        # Normalize x-limits for readability
        xmax = max(vals) if vals else 1
        ax_bar.set_xlim(0, xmax * 1.15)
    else:
        ax_bar.text(0.5, 0.5, "수치형 지표 없음", ha="center", va="center", fontsize=9)
        ax_bar.set_xticks([])
        ax_bar.set_yticks([])

    ax_bar.grid(axis="x", alpha=0.2, linestyle=":")

    # Text panel: key=value compact list
    ax_txt.axis("off")
    lines = []
    for k in keys:
        lines.append(f"• {k}: {metrics.get(k)}")
    txt = "\n".join(lines[:8])
    ax_txt.text(0, 0.95, "지표", fontsize=10, fontweight="bold", va="top")
    ax_txt.text(0, 0.88, txt or "(지표 데이터 없음)", fontsize=9, va="top")

    fig.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def render_customs_flow_png(company, country):
    """Draw a simple cross-border logistics/customs flow with boxes and arrows."""
    os.makedirs(f"outputs/{company}_{country}", exist_ok=True)
    path = f"outputs/{company}_{country}/02_customs_flow_{company}_{country}.png"

    _set_kr_font()
    fig, ax = plt.subplots(figsize=(8, 2.8))
    ax.set_title(f"Customs/Logistics Flow | {company} - {country}", fontsize=11)
    ax.axis("off")

    steps = [
        ("Seller\n(Exporter)",),
        ("Broker/FF",),
        (f"Customs\n({country})",),
        ("3PL / WH",),
        ("CEP / Last Mile",),
        ("Consumer",),
    ]

    # layout
    n = len(steps)
    x0, x1 = 0.05, 0.95
    ys = 0.5
    xs = [x0 + i * (x1 - x0) / (n - 1) for i in range(n)]

    # Draw boxes and arrows
    box_w, box_h = 0.12, 0.35
    for i, (label,) in enumerate(steps):
        rect = patches.FancyBboxPatch(
            (xs[i] - box_w / 2, ys - box_h / 2),
            box_w,
            box_h,
            boxstyle="round,pad=0.02,rounding_size=0.02",
            linewidth=1.2,
            edgecolor="#3C3C3C",
            facecolor="#F2F6FF" if i not in (2,) else "#E6FFFB",
        )
        ax.add_patch(rect)
        ax.text(xs[i], ys, label, ha="center", va="center", fontsize=9)
        if i < n - 1:
            ax.annotate(
                "",
                xy=(xs[i + 1] - box_w / 2, ys),
                xytext=(xs[i] + box_w / 2, ys),
                arrowprops=dict(arrowstyle="->", lw=1.2, color="#6A6A6A"),
            )

    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path
