import csv
import os
from ..state_schema import State, RegulationCompliance, RegulationItem
from ..viz.charts import render_customs_flow_png

# Per spec: NICE is excluded from coverage (weight 0)
WEIGHT = {"MUST": 3, "SHOULD": 2, "NICE": 0}
SCORE = {"PASS": 1.0, "WARN": 0.5, "TBD": 0.0, "FAIL": 0.0}


def compute_coverage(items):
    num = den = tbd = 0
    blocker = False
    for it in items:
        if it.applicability == "NA":
            continue
        w = WEIGHT.get(it.criticality, 0)
        s = SCORE.get(it.status, 0)
        num += w * s
        den += w
        if it.status == "TBD":
            tbd += w
        if it.criticality == "MUST" and it.status == "FAIL":
            blocker = True
    cov = (num / den) if den else 0.0
    tbd_ratio = (tbd / den) if den else 0.0
    return cov, blocker, tbd_ratio


def _load_items(country: str):
    path = os.path.join("data", "regulation", f"{country}.csv")
    items = []
    if os.path.exists(path):
        try:
            with open(path, newline="", encoding="utf-8") as f:
                r = csv.DictReader(f)
                for row in r:
                    items.append(
                        RegulationItem(
                            id=row.get("id", "").strip() or row.get("title", "").strip(),
                            category=row.get("category", "").strip() or "General",
                            title=row.get("title", "").strip(),
                            criticality=(row.get("criticality", "MUST").strip().upper()),
                            applicability=(row.get("applicability", "APPLIES").strip().upper()),
                            status=(row.get("status", "TBD").strip().upper()),
                            evidence=(
                                [{"url": row.get("evidence_url", "").strip()}]
                                if row.get("evidence_url") else []
                            ),
                            notes=row.get("notes", "").strip(),
                        )
                    )
        except Exception:
            items = []
    # Fallback minimal checklist
    if not items:
        items = [
            RegulationItem(id="LICENSE", category="License", title="3PL broker license", criticality="MUST", applicability="APPLIES", status="PASS"),
            RegulationItem(id="DATA_XFER", category="Data", title="Personal data cross-border transfer", criticality="MUST", applicability="APPLIES", status="TBD"),
            RegulationItem(id="REFUND", category="Ecom", title="Refund/return notice", criticality="SHOULD", applicability="APPLIES", status="PASS"),
            RegulationItem(id="AD_MARK", category="Ecom", title="Advertising disclosure", criticality="SHOULD", applicability="APPLIES", status="WARN"),
            RegulationItem(id="FTZ", category="Customs", title="Free trade zone benefits", criticality="NICE", applicability="NA", status="TBD"),
        ]
    return items


def run(state: State, ctx):
    items = _load_items(ctx["country"])
    cov, blocker, tbd_ratio = compute_coverage(items)
    png = render_customs_flow_png(ctx["company"]["name"], ctx["country"])
    # Risk badge heuristic
    if blocker or cov < 0.8:
        badge = "High"
    elif cov < 0.9 or tbd_ratio >= 0.2:
        badge = "Medium"
    else:
        badge = "Low"

    state.reg_compliance = RegulationCompliance(
        items=items,
        coverage=cov,
        blocker=blocker,
        customs_flow_png=png,
        tbd_ratio=tbd_ratio,
        risk_badge=badge,
    )

