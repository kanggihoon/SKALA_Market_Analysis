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
        w = WEIGHT[it.criticality]
        s = SCORE[it.status]
        num += w * s
        den += w
        if it.status == "TBD":
            tbd += w
        if it.criticality == "MUST" and it.status == "FAIL":
            blocker = True
    cov = (num / den) if den else 0.0
    tbd_ratio = (tbd / den) if den else 0.0
    return cov, blocker, tbd_ratio


def run(state: State, ctx):
    # TODO: 실제 체크리스트 구성
    items = [
        RegulationItem(
            id="LICENSE",
            category="License",
            title="택배업/3PL 신고",
            criticality="MUST",
            applicability="APPLIES",
            status="PASS",
        ),
        RegulationItem(
            id="DATA_XFER",
            category="Data",
            title="개인정보 국외이전",
            criticality="MUST",
            applicability="APPLIES",
            status="TBD",
        ),
        RegulationItem(
            id="REFUND_NOTICE",
            category="Ecom",
            title="환불/반품 고지",
            criticality="SHOULD",
            applicability="APPLIES",
            status="PASS",
        ),
        RegulationItem(
            id="AD_MARK",
            category="Ecom",
            title="표시광고 가이드",
            criticality="SHOULD",
            applicability="APPLIES",
            status="WARN",
        ),
        RegulationItem(
            id="FTZ",
            category="Customs",
            title="FTZ 특례",
            criticality="NICE",
            applicability="NA",
            status="TBD",
        ),
    ]
    cov, blocker, tbd_ratio = compute_coverage(items)
    png = render_customs_flow_png(ctx["company"]["name"], ctx["country"])
    # Risk badge heuristic
    if blocker or cov < 0.8:
        badge = "높음"
    elif cov < 0.9 or tbd_ratio >= 0.2:
        badge = "보통"
    else:
        badge = "낮음"

    state.reg_compliance = RegulationCompliance(
        items=items,
        coverage=cov,
        blocker=blocker,
        customs_flow_png=png,
        tbd_ratio=tbd_ratio,
        risk_badge=badge,
    )
    # tbd_ratio는 decision에서 사용 (필요시 state.artifacts 등 저장 가능)
