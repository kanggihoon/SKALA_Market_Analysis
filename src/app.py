import json
import argparse
import sys
import os
import warnings
from pathlib import Path

# Allow running as script: `python src/app.py ...`
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Apply matplotlib settings early
try:
    import matplotlib  # type: ignore
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt  # type: ignore
    plt.rcParams['axes.unicode_minus'] = False
    try:
        matplotlib.set_loglevel("error")
    except Exception:
        pass
except Exception:
    plt = None  # type: ignore

from loguru import logger
from dotenv import load_dotenv
from src.viz.fonts import ensure_kr_font
from src.state_schema import State
from src.graph.build_graph import run_pipeline


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="data/companies.json")
    parser.add_argument("--out", required=True, help="outputs/")
    parser.add_argument("--phase", default="phase1", choices=["phase1", "full"], help="pipeline phase to run")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        meta = json.load(f)

    # Load environment variables from possible locations
    loaded_paths = []
    candidates = [
        ROOT / ".env",
        Path.cwd() / ".env",
        ROOT.parent / ".env",
        ROOT / ".env.local",
    ]
    for p in candidates:
        if p.exists():
            if load_dotenv(dotenv_path=p, override=False):
                loaded_paths.append(str(p))
    if loaded_paths:
        logger.info("Loaded .env from: {}", loaded_paths)
    else:
        logger.info("No .env file found in {}", [str(ROOT), str(Path.cwd()), str(ROOT.parent)])

    # Log masked presence of Google key
    gkey = os.getenv("GOOGLE_MAPS_API_KEY")
    if gkey:
        try:
            masked = f"{gkey[:6]}…{gkey[-4:]}"
        except Exception:
            masked = "***masked***"
        logger.info("GOOGLE_MAPS_API_KEY detected: {}", masked)
    else:
        logger.warning("GOOGLE_MAPS_API_KEY not found in environment. Maps will use fallback.")

    # Set fonts early and suppress glyph warnings
    selected = ensure_kr_font()
    if selected:
        logger.info("Matplotlib font set: {} (unicode_minus=False)", selected)

    warnings.filterwarnings(
        "ignore",
        message=r"Font '.*' does not have a glyph for '\\u2212'",
        category=UserWarning,
    )
    warnings.filterwarnings(
        "ignore",
        message=r"Glyph .* missing from font\(s\).*",
        category=UserWarning,
    )

    state = State()
    logger.info("Starting pipeline for {} companies", len(meta.get("companies", [])))
    run_pipeline(state, meta, args.out, phase=args.phase)


if __name__ == "__main__":
    main()
