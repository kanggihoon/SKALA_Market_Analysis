from ..state_schema import State, SegmentCard


def run(state: State, ctx):
    state.gtm_high = SegmentCard(
        icp="엔터프라이즈/대형 셀러",
        offer="전담 풀필+SLA+규제패키지",
        price_hint="ACV 100k~500k",
        channel="파트너+직접(High-touch)",
        kpi={"growth": "SQL", "conv": "Win%", "quality": "OTD"},
        risks=["롱세일즈", "구현 복잡"],
    )

