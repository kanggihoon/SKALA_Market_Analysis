from ..state_schema import State, Risks


def run(state: State, ctx):
    cov = state.reg_compliance.coverage if state.reg_compliance else 0.0
    tbd = state.reg_compliance.tbd_ratio if state.reg_compliance else 0.0
    partners_n = len(state.partners.candidates) if state.partners and state.partners.candidates else 0

    register = []
    if cov < 0.8:
        register.append({
            "risk": "Regulatory coverage gap",
            "prob": "M",
            "impact": "H",
            "mitigation": "Prioritize MUST items; engage local counsel",
            "trigger": "coverage<0.8",
        })
    if tbd >= 0.2:
        register.append({
            "risk": "High TBD ratio",
            "prob": "M",
            "impact": "M",
            "mitigation": "Accelerate evidence collection and PoCs",
            "trigger": "tbd_ratio>=0.2",
        })
    if partners_n < 2:
        register.append({
            "risk": "Limited partner footprint",
            "prob": "M",
            "impact": "M",
            "mitigation": "Add 3PL/customs shortlist and outreach",
            "trigger": "partners<2",
        })

    thresholds = {"coverage_min": 0.8, "tbd_ratio_max": 0.2}
    state.risks = Risks(register_items=register, thresholds=thresholds)

