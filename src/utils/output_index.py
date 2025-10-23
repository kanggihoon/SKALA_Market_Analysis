import os
import json
from pathlib import Path


def build_outputs_index(out_dir: str) -> None:
    root = Path(out_dir)
    rows = []
    links = []
    for p in sorted(root.glob("*_*")):
        if not p.is_dir():
            continue
        summary = p / "summary.json"
        card = next(p.glob("strategy_card_*.md"), None)
        if summary.exists():
            try:
                data = json.loads(summary.read_text(encoding="utf-8"))
                rows.append({
                    "name": p.name,
                    "decision": data.get("decision"),
                    "final": data.get("final"),
                    "coverage": data.get("coverage"),
                    "tbd_ratio": data.get("tbd_ratio"),
                    "risk_badge": data.get("risk_badge"),
                    "gtm": data.get("gtm_selected"),
                    "card": str((p / data.get("card", "")).relative_to(root)) if data.get("card") else (str(card.relative_to(root)) if card else None),
                    "html": str((p / f"strategy_card_{p.name}.html").relative_to(root)) if (p / f"strategy_card_{p.name}.html").exists() else None,
                })
            except Exception:
                pass
        elif card:
            links.append((p.name, str(card.relative_to(root))))

    lines = ["# Outputs Index", "", "자동 생성된 전략 카드 요약", ""]
    if rows:
        lines.append("| Case | Decision | Final | Coverage | TBD | Risk | GTM | Card | HTML |")
        lines.append("|---|---|---:|---:|---:|---|---|---|---|")
        for r in rows:
            cov = f"{r['coverage']*100:.0f}%" if isinstance(r.get('coverage'), (int, float)) else ""
            tbd = f"{r['tbd_ratio']*100:.0f}%" if isinstance(r.get('tbd_ratio'), (int, float)) else ""
            html_link = r.get('html','')
            html_cell = f"[{html_link}]({html_link})" if html_link else ""
            lines.append(f"| {r['name']} | {r.get('decision','')} | {r.get('final','')} | {cov} | {tbd} | {r.get('risk_badge','')} | {r.get('gtm','')} | [{r.get('card','')}]({r.get('card','')}) | {html_cell} |")
        lines.append("")
    if links:
        lines.append("## Cards")
        for name, rel in links:
            lines.append(f"- {name}: [{rel}]({rel})")

    (root / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
