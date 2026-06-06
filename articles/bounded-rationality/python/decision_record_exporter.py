#!/usr/bin/env python3
"""Decision record exporter for bounded rationality."""

from __future__ import annotations

from pathlib import Path
import json

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
RECORDS = ARTICLE_ROOT / "outputs" / "decision_records"


def main() -> None:
    RECORDS.mkdir(parents=True, exist_ok=True)
    record = {
        "article": "Bounded Rationality",
        "decision_context": "",
        "decision_owner": "",
        "constraints": {
            "information": [],
            "time": [],
            "attention": [],
            "organizational_capacity": [],
            "implementation": []
        },
        "alternatives_searched": [],
        "excluded_search_space": [],
        "aspiration_thresholds": [],
        "search_rule": "",
        "stopping_rule": "",
        "selected_action": "",
        "optimizing_benchmark": None,
        "opportunity_loss": None,
        "search_cost": None,
        "net_value": None,
        "dissent": [],
        "review_triggers": [],
        "post_decision_learning": []
    }
    path = RECORDS / "bounded_rationality_decision_record_template.json"
    path.write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()
