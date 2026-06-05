#!/usr/bin/env python3
"""Decision-record exporter template for historical decision paradigms."""

from __future__ import annotations

from pathlib import Path
import json

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
RECORDS = ARTICLE_ROOT / "outputs" / "decision_records"


def main() -> None:
    RECORDS.mkdir(parents=True, exist_ok=True)
    record = {
        "article": "The History of Decision Science",
        "historical_paradigm": "",
        "decision_rule": "",
        "assumptions": [],
        "probability_model": "",
        "utility_model": "",
        "selected_strategy": "",
        "review_triggers": [],
    }
    path = RECORDS / "historical_decision_record_template.json"
    path.write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()
