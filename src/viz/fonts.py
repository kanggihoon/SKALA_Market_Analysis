import os
from matplotlib import pyplot as plt
from matplotlib import font_manager
from matplotlib.font_manager import FontProperties


def ensure_kr_font() -> str:
    """Best-effort: register a KR-capable font and set rcParams.

    Returns the selected family name (or empty string if unknown).
    """
    # Prefer Nanum or Malgun if present
    candidates = [
        r"C:\\Windows\\Fonts\\NanumGothic.ttf",
        r"C:\\Windows\\Fonts\\NanumGothicBold.ttf",
        r"C:\\Windows\\Fonts\\malgun.ttf",
        r"C:\\Windows\\Fonts\\malgunbd.ttf",
        r"/System/Library/Fonts/AppleSDGothicNeo.ttc",
        r"/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        r"/usr/share/fonts/truetype/noto/NotoSansCJKkr-Regular.otf",
        r"/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                font_manager.fontManager.addfont(path)
                family = FontProperties(fname=path).get_name()
                if family:
                    plt.rcParams["font.family"] = family
                    plt.rcParams["axes.unicode_minus"] = False
                    plt.rcParams["figure.dpi"] = 100
                    plt.rcParams["savefig.dpi"] = 100
                    return family
            except Exception:
                continue

    # Fallback to common family names (may still warn if missing)
    plt.rcParams["font.family"] = ["NanumGothic", "Malgun Gothic", "AppleGothic", "Noto Sans CJK KR", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["figure.dpi"] = 100
    plt.rcParams["savefig.dpi"] = 100
    return ""
