#!/usr/bin/env python3
"""Decision-record template for uncertainty-aware decisions."""

from __future__ import annotations

from pathlib import Path
import json

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
RECORDS = ARTICLE_ROOT / "outputs" / "decision_records"


def main() -> None:
    RECORDS.mkdir(parents=True, exist_ok=True)
    record = {
        "article": "Why Uncertainty Changes Decision-Making",
        "decision_context": "",
        "uncertainty_type": ["risk", "ambiguity", "deep uncertainty"],
        "alternatives": [],
        "scenarios": [],
        "assumptions": [],
        "decision_rule": "",
        "selected_strategy": "",
        "monitoring_indicators": [],
        "review_triggers": [],
    }
    path = RECORDS / "uncertainty_decision_record_template.json"
    path.write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()
