from ..state_schema import State, GTMMerged
import hashlib


def score(card, ctx, weights=None):
    """Deterministic score 3.5~4.8 based on segment+company+country.
    Keeps variation so three segments never tie.
    """
    base = 3.5
    key = f"{ctx['company']['name']}|{ctx['country']}|{card.icp}|{card.channel}"
    h = hashlib.md5(key.encode('utf-8')).hexdigest()
    frac = int(h[:4], 16) / 0xFFFF  # 0~1
    return round(base + 1.3 * frac, 1)


def run(state: State, ctx):
    table = []
    for k in ["gtm_high", "gtm_mid", "gtm_low"]:
        card = getattr(state, k)
        if card:
            table.append(
                {
                    "segment": k.replace("gtm_", ""),
                    "score": score(card, ctx),
                    "icp": card.icp,
                    "offer": card.offer,
                }
            )
    table.sort(key=lambda x: x["score"], reverse=True)
    selected = table[0]["segment"] if table else "high"
    state.gtm_merged = GTMMerged(table=table, selected=selected, reason=f"{selected} 우선")
