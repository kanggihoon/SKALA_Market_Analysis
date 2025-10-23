from ..state_schema import State, Competition
from ..viz.maps import render_competition_heatmap
from ..utils.competitor_data import load_competitor_entities


def run(state: State, ctx):
    company = ctx["company"]["name"]
    country = ctx["country"]
    comps = load_competitor_entities(company, country) or []
    # Pass full entities so renderer can colorize by category
    heatmap_png, markers_map_png, positioning, whitespaces = render_competition_heatmap(
        company, country, comps if comps else None
    )
    if comps:
        positioning = {**positioning, "entities": comps}
    state.competition = Competition(
        heatmap_png=heatmap_png,
        markers_map_png=markers_map_png,
        positioning=positioning,
        whitespaces=whitespaces,
    )
