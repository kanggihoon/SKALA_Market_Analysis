from ..state_schema import State, SegmentCard


def run(state: State, ctx):
    state.gtm_low = SegmentCard(
        icp="SMB / emerging sellers",
        offer="Self-serve platform + basic support",
        price_hint="ARPA 200–800",
        channel="Product-led growth (PLG)",
        kpi={"growth": "Signups", "conv": "Paid%", "quality": "CSAT"},
        risks=["Churn risk", "Low ARPA"],
    )

