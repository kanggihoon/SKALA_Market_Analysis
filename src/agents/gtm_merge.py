from ..state_schema import State, GTMMerged
import hashlib


def _jitter(ctx, segment: str) -> float:
    key = f"{ctx['company']['name']}|{ctx['country']}|{segment}"
    h = hashlib.md5(key.encode('utf-8')).hexdigest()
    frac = int(h[:4], 16) / 0xFFFF  # 0~1
    return (frac - 0.5) * 0.4  # -0.2..+0.2


def score_segment(state: State, segment: str, ctx) -> float:
    cov = state.reg_compliance.coverage if state.reg_compliance else 0.0
    tbd = state.reg_compliance.tbd_ratio if state.reg_compliance else 0.0
    whites = (len(state.competition.whitespaces) if state.competition and state.competition.whitespaces else 0)
    partners_n = len(state.partners.candidates) if state.partners and state.partners.candidates else 0

    s = 3.0
    # Coverage impact
    if cov >= 0.9:
        s += 0.5
    elif cov >= 0.8:
        s += 0.2
    else:
        s -= 0.3
    # TBD penalty
    if tbd >= 0.2:
        s -= 0.2
    # Competition whitespace
    if whites >= 2:
        s += 0.2
    # Partner readiness
    if partners_n >= 2:
        s += 0.2
    # Segment preferences (example: high slightly favors enterprise readiness)
    seg_bias = {"high": 0.1, "mid": 0.0, "low": -0.05}.get(segment, 0.0)
    s += seg_bias
    s += _jitter(ctx, segment)
    return round(max(2.5, min(5.0, s)), 1)


def run(state: State, ctx):
    table = []
    for k in ["gtm_high", "gtm_mid", "gtm_low"]:
        card = getattr(state, k)
        if card:
            seg = k.replace("gtm_", "")
            table.append(
                {
                    "segment": seg,
                    "score": score_segment(state, seg, ctx),
                    "icp": card.icp,
                    "offer": card.offer,
                }
            )
    table.sort(key=lambda x: x["score"], reverse=True)
    selected = table[0]["segment"] if table else "high"
    state.gtm_merged = GTMMerged(table=table, selected=selected, reason=f"{selected} 우선")
