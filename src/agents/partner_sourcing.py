import csv
import os
from ..state_schema import State, Partners
from ..viz.maps import render_partner_map


def _load_partners(country: str):
    path = os.path.join("data", "partners", f"{country}.csv")
    candidates = []
    if os.path.exists(path):
        try:
            with open(path, newline="", encoding="utf-8") as f:
                r = csv.DictReader(f)
                for row in r:
                    candidates.append({
                        "name": row.get("name", "").strip(),
                        "role": row.get("role", "").strip() or "",
                        "priority": row.get("priority", "").strip() or "Mid",
                    })
        except Exception:
            candidates = []
    if not candidates:
        candidates = [
            {"name": "ABC Customs", "role": "Customs", "priority": "High"},
            {"name": "XYZ 3PL", "role": "3PL", "priority": "Mid"},
            {"name": "SI-One", "role": "SI", "priority": "Mid"},
        ]
    return [c for c in candidates if c.get("name")]


def run(state: State, ctx):
    candidates = _load_partners(ctx["country"])
    png = render_partner_map(ctx["company"]["name"], ctx["country"], candidates)
    state.partners = Partners(candidates=candidates, partner_map_png=png)

