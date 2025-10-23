from ..state_schema import State, Risks


def run(state: State, ctx):
    register = [
        {"risk": "규제 해석 지연", "prob": "M", "impact": "H", "mitigation": "로펌 의견서", "trigger": "coverage<0.8"},
        {"risk": "SLA 미달", "prob": "M", "impact": "M", "mitigation": "대체 3PL", "trigger": "OTD<95%"},
    ]
    thresholds = {"coverage_min": 0.8, "otd_min": 0.95}
    state.risks = Risks(register_items=register, thresholds=thresholds)
