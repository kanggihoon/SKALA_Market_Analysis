from ..state_schema import State, SegmentCard


def run(state: State, ctx):
    state.gtm_high = SegmentCard(
        icp="Enterprise eCommerce / 3PL integrators",
        offer="Premium cross-border SLA + compliance support",
        price_hint="ACV 100k–500k",
        channel="Direct sales (high-touch)",
        kpi={"growth": "SQL", "conv": "Win%", "quality": "OTD"},
        risks=["Long sales cycle", "High onboarding cost"],
    )

