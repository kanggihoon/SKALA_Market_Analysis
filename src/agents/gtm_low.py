from ..state_schema import State, SegmentCard


def run(state: State, ctx):
    state.gtm_low = SegmentCard(
        icp="SMB/크로스보더 시범",
        offer="셀프서비스+라이트 풀필",
        price_hint="ARPA 200~800",
        channel="온라인/마켓플레이스",
        kpi={"growth": "Signups", "conv": "Paid%", "quality": "CSAT"},
        risks=["이탈률", "단가 낮음"],
    )

