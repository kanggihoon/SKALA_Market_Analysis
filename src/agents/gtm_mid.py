from ..state_schema import State, SegmentCard


def run(state: State, ctx):
    state.gtm_mid = SegmentCard(
        icp="Mid-market brands / regional D2C",
        offer="Standardized cross-border suite with tiered support",
        price_hint="ACV 20k–80k",
        channel="Partner-led + inside sales",
        kpi={"growth": "MQL", "conv": "SQO%", "quality": "NPS"},
        risks=["Pricing pressure", "Category competition"],
    )

