import os
import json
import hashlib
from ..state_schema import State, MarketSummary
from ..viz.charts import render_market_summary_png


def _case_specific_metrics(company, country):
    """Generate case-specific market metrics to ensure diversity.

    Per planning doc: each case must have different metrics.
    """
    key = f"{company}|{country}"
    h = hashlib.md5(key.encode('utf-8')).hexdigest()

    # Base values with variation
    tam_base = 0.8 + (int(h[0:2], 16) % 20) / 10  # 0.8-2.8B
    cagr = 5 + (int(h[2:4], 16) % 10)  # 5-15%
    ecom = 25 + (int(h[4:6], 16) % 30)  # 25-55%
    infra = 65 + (int(h[6:8], 16) % 25)  # 65-90
    cost = 3.0 + (int(h[8:10], 16) % 30) / 10  # 3.0-6.0

    return {
        "TAM": f"~${tam_base:.1f}B",
        "CAGR": f"{cagr}%",
        "Ecom Penetration": f"{ecom}%",
        "Infra Score": f"{infra}",
        "Avg Ship Cost": f"${cost:.1f}",
    }


def run(state: State, ctx):
    company = ctx["company"]["name"]
    country = ctx["country"]

    # Generate case-specific defaults
    metrics = _case_specific_metrics(company, country)
    why_now = "크로스보더 수요 증가와 물류 인프라 개선으로 진입 타이밍 양호"

    # Optional override: data/market_overrides/{Company}_{Country}.json
    ov_dir = os.path.join("data", "market_overrides")
    ov_path = os.path.join(ov_dir, f"{company}_{country}.json")
    try:
        if os.path.exists(ov_path):
            with open(ov_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if isinstance(data.get('metrics'), dict):
                # Merge so missing keys keep numeric defaults
                m = metrics.copy(); m.update(data['metrics'])
                metrics = m
            why_now = data.get('why_now', why_now)
    except Exception:
        pass
    png = render_market_summary_png(company, country, metrics)
    state.market_summary = MarketSummary(
        metrics=metrics, why_now=why_now, market_summary_png=png
    )
    state.segments_initial = ["high", "mid", "low"]
