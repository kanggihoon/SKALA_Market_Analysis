from ..state_schema import State, SegmentCard


def run(state: State, ctx):
    state.gtm_mid = SegmentCard(
        icp="중견/성장 셀러",
        offer="표준 풀필+가이드 킷",
        price_hint="ACV 20k~80k",
        channel="파트너+온라인 세일즈",
        kpi={"growth": "MQL", "conv": "SQO%", "quality": "NPS"},
        risks=["가격 민감", "로컬 경쟁"],
    )

