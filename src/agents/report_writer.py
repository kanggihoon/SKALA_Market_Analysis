import os
import json
from ..state_schema import State
from jinja2 import Template


CARD_TMPL = """# {{company}} × {{country}} Market Entry
## Executive
- Decision: **{{decision.status}}** ({{decision.reason}})
- Regulation Coverage: {{cov_pct}}% (TBD {{tbd_pct}}%, Risk={{risk_badge}})
- Chosen GTM: {{gtm_selected}}

## Market
- Why Now: {{why_now}}
- Metrics: {{metrics}}
{% if market_png %}
![]({{market_png}})
{% endif %}

## Regulation
- Blocker: {{blocker}}
{% if customs_png %}
![]({{customs_png}})
{% endif %}

## Competition
- Whitespaces
{% for w in whitespaces %}- {{w}}
{% endfor %}
{% if heatmap %}
### Competition Heatmap
![]({{heatmap}})
{% endif %}
{% if markers_map %}
### Competitor Map
![]({{markers_map}})
{% endif %}

## GTM
- Selected: {{gtm_selected}}

| Segment | Score | ICP | Offer |
|---|---:|---|---|
{% for row in gtm_table %}| {{row.segment}} | {{"%.1f"|format(row.score)}} | {{row.icp}} | {{row.offer}} |
{% endfor %}

## Partners
{% for p in partners %}- {{p.name}} ({{p.role}}) · priority={{p.priority}}
{% endfor %}
{% if partner_map %}
![]({{partner_map}})
{% endif %}

## Risks
{% for r in risks %}- {{r.risk}} · prob={{r.prob}} · impact={{r.impact}} · mitigation={{r.mitigation}} (trigger: {{r.trigger}})
{% endfor %}

## Decision Scorecard
| key | value |
|---|---|
| base | {{scorecard.base}} |
| coverage | {{scorecard.cov}} |
| tbd_ratio | {{scorecard.tbd_ratio}} |
| competition_high | {{scorecard.competition_high}} |
| partners | {{scorecard.partners}} |
| final | **{{scorecard.final}}** |
"""


def run(state: State, ctx):
    company, country, out_dir = ctx["company"]["name"], ctx["country"], ctx["out_dir"]
    out = os.path.join(out_dir, f"{company}_{country}")
    os.makedirs(out, exist_ok=True)

    cov = state.reg_compliance.coverage if state.reg_compliance else 0
    tbd = state.reg_compliance.tbd_ratio if state.reg_compliance else 0
    badge = state.reg_compliance.risk_badge if state.reg_compliance else ""
    gtm_sel = state.gtm_merged.selected if state.gtm_merged else "high"

    def bn(p):
        return os.path.basename(p) if p else None

    market_png = bn(state.market_summary.market_summary_png if state.market_summary else None)
    customs_png = bn(state.reg_compliance.customs_flow_png if state.reg_compliance else None)
    heatmap = bn(state.competition.heatmap_png if state.competition else None)
    markers_map = bn(getattr(state.competition, 'markers_map_png', None) if state.competition else None)
    partner_map = bn(state.partners.partner_map_png if state.partners else None)

    class Row(dict):
        __getattr__ = dict.get

    table = [Row(**r) for r in (state.gtm_merged.table if state.gtm_merged else [])]

    t = Template(CARD_TMPL)
    md = t.render(
        company=company,
        country=country,
        decision=state.decision,
        cov_pct=round(cov * 100),
        tbd_pct=round(tbd * 100),
        risk_badge=badge,
        gtm_selected=gtm_sel,
        why_now=(state.market_summary.why_now if state.market_summary else ""),
        metrics=(state.market_summary.metrics if state.market_summary else {}),
        blocker=(state.reg_compliance.blocker if state.reg_compliance else False),
        customs_png=customs_png,
        market_png=market_png,
        whitespaces=(state.competition.whitespaces if state.competition else []),
        heatmap=heatmap,
        markers_map=markers_map,
        gtm_table=table,
        partners=(state.partners.candidates if state.partners else []),
        partner_map=partner_map,
        risks=(state.risks.register_items if state.risks else []),
        scorecard=(state.decision.scorecard if state.decision else {}),
    )
    with open(os.path.join(out, f"strategy_card_{company}_{country}.md"), "w", encoding="utf-8") as f:
        f.write(md)

    # Summary JSON for indexers
    summary = {
        "company": company,
        "country": country,
        "decision": (state.decision.status if state.decision else None),
        "final": (state.decision.scorecard.get("final") if state.decision else None),
        "coverage": cov,
        "tbd_ratio": tbd,
        "risk_badge": badge,
        "gtm_selected": gtm_sel,
        "card": f"strategy_card_{company}_{country}.md",
    }
    with open(os.path.join(out, "summary.json"), "w", encoding="utf-8") as sf:
        json.dump(summary, sf, ensure_ascii=False, indent=2)

    # Rich case state for DOCX builder
    case_state = {
        "company": company,
        "country": country,
        "decision": (state.decision.dict() if state.decision else {}),
        "coverage": cov,
        "tbd_ratio": tbd,
        "risk_badge": badge,
        "market": {
            "why_now": (state.market_summary.why_now if state.market_summary else ""),
            "metrics": (state.market_summary.metrics if state.market_summary else {}),
        },
        "competition": {
            "whitespaces": (state.competition.whitespaces if state.competition else []),
            "entities": (getattr(state.competition, 'positioning', {}).get('entities', []) if state.competition and isinstance(getattr(state.competition, 'positioning', {}), dict) else []),
        },
        "gtm": {
            "table": (state.gtm_merged.table if state.gtm_merged else []),
            "selected": gtm_sel,
        },
        "partners": (state.partners.candidates if state.partners else []),
        "risks": (state.risks.register_items if state.risks else []),
        "images": {
            "market": market_png,
            "customs": customs_png,
            "heatmap": heatmap,
            "partner": partner_map,
        },
    }
    with open(os.path.join(out, "case_state.json"), "w", encoding="utf-8") as cf:
        json.dump(case_state, cf, ensure_ascii=False, indent=2)

