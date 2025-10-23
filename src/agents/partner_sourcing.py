from ..state_schema import State, Partners
from ..viz.maps import render_partner_map


def run(state: State, ctx):
    # 경쟁 밀집권역 기반 후보 발굴 (스텁)
    candidates = [
        {"name": "ABC Customs", "role": "Customs", "priority": "High"},
        {"name": "XYZ 3PL", "role": "3PL", "priority": "Mid"},
        {"name": "SI-One", "role": "SI", "priority": "Mid"},
    ]
    png = render_partner_map(ctx["company"]["name"], ctx["country"], candidates)
    state.partners = Partners(candidates=candidates, partner_map_png=png)

