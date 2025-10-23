import os
import json
from ..state_schema import State, MarketSummary
from ..viz.charts import render_market_summary_png


def run(state: State, ctx):
    # Defaults (ensure numeric-friendly values for charts)
    metrics = {
        "TAM": "~$1.2B",
        "CAGR": "8%",
        "Ecom Penetration": "34%",
        "Infra Score": "78",
        "Avg Ship Cost": "$4.2",
    }
    why_now = (
        "Cross-border growth tailwinds: ecom penetration up, logistics infra maturing, and cost curves improving."
    )

    # Optional override: data/market_overrides/{Company}_{Country}.json
    ov_dir = os.path.join("data", "market_overrides")
    ov_path = os.path.join(ov_dir, f"{ctx['company']['name']}_{ctx['country']}.json")
    try:
        if os.path.exists(ov_path):
            with open(ov_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if isinstance(data.get('metrics'), dict):
                m = metrics.copy(); m.update(data['metrics'])
                metrics = m
            why_now = data.get('why_now', why_now)
    except Exception:
        pass
    png = render_market_summary_png(ctx["company"]["name"], ctx["country"], metrics)
    state.market_summary = MarketSummary(
        metrics=metrics, why_now=why_now, market_summary_png=png
    )
    state.segments_initial = ["high", "mid", "low"]

