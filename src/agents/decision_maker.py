from ..state_schema import State, Decision


def run(state: State, ctx):
    cov = state.reg_compliance.coverage if state.reg_compliance else 0.0
    tbd_ratio = (
        state.reg_compliance.tbd_ratio if state.reg_compliance and hasattr(state.reg_compliance, "tbd_ratio") else 0.0
    )
    blocker = state.reg_compliance.blocker if state.reg_compliance else False

    # Base per spec
    score = 70

    # Coverage adjustments
    if cov >= 0.90:
        score += 10
    elif cov < 0.80:
        score -= 20
    if tbd_ratio >= 0.20:
        score -= 5

    # Competition penalty: if no whitespace opportunities detected (high competition)
    high_comp = False
    try:
        whites = state.competition.whitespaces if state.competition else []
        high_comp = (len(whites) == 0)
    except Exception:
        high_comp = False
    if high_comp:
        score -= 10

    # Feasibility boost: at least 2 partners
    partners_n = len(state.partners.candidates) if state.partners and state.partners.candidates else 0
    if partners_n >= 2:
        score += 20

    if blocker:
        state.decision = Decision(
            status="HOLD",
            scorecard={
                "base": 70,
                "cov": cov,
                "tbd_ratio": tbd_ratio,
                "competition_high": high_comp,
                "partners": partners_n,
                "final": 0,
                "blocker": True,
            },
            reason="MUST item FAIL → HOLD",
        )
        return

    status = "RECOMMEND" if score >= 60 else "HOLD"
    state.decision = Decision(
        status=status,
        scorecard={
            "base": 70,
            "cov": cov,
            "tbd_ratio": tbd_ratio,
            "competition_high": high_comp,
            "partners": partners_n,
            "final": score,
        },
        reason=f"coverage={cov:.0%}, TBD={tbd_ratio:.0%}, score={score}",
    )

