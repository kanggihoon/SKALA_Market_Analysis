import csv
from pathlib import Path
from typing import List, Dict


def load_competitor_entities(company: str, country: str) -> List[Dict[str, str]]:
    """Load competitor entities from CSVs under data/rag_corpus/competition.

    Expected header: company,target_market,competitor,category,homepage
    Returns list of dicts with keys: name, category, homepage.
    """
    base = Path(__file__).resolve().parents[3] / "data" / "rag_corpus" / "competition"
    entities: List[Dict[str, str]] = []
    if not base.exists():
        return entities
    for csv_path in base.glob("*.csv"):
        try:
            with open(csv_path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if not row:
                        continue
                    if row.get("company") and row.get("target_market"):
                        if row["company"].strip().lower() == company.strip().lower() and row[
                            "target_market"
                        ].strip().upper() == country.strip().upper():
                            entities.append(
                                {
                                    "name": row.get("competitor", "").strip(),
                                    "category": row.get("category", "").strip(),
                                    "homepage": row.get("homepage", "").strip(),
                                }
                            )
        except Exception:
            continue
    return [e for e in entities if e.get("name")]

