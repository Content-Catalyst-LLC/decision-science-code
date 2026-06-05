#!/usr/bin/env python3
"""Decision-record exporter template."""

from __future__ import annotations

from pathlib import Path
import json

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
RECORDS = ARTICLE_ROOT / "outputs" / "decision_records"


def main() -> None:
    RECORDS.mkdir(parents=True, exist_ok=True)
    record = {
        "article": "Decision Science vs. Decision Theory",
        "formal_model": {
            "actions": [],
            "states": [],
            "probabilities": [],
            "utilities": [],
        },
        "applied_context": {
            "evidence_quality": [],
            "implementation_constraints": [],
            "stakeholder_legitimacy": [],
            "review_triggers": [],
        },
    }
    path = RECORDS / "decision_theory_science_template.json"
    path.write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()
