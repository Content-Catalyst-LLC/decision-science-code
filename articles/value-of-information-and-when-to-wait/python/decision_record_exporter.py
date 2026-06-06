#!/usr/bin/env python3
"""Decision record exporter for value of information and waiting."""

from __future__ import annotations

from pathlib import Path
import json

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
RECORDS = ARTICLE_ROOT / "outputs" / "decision_records"


def main() -> None:
    RECORDS.mkdir(parents=True, exist_ok=True)
    record = {
        "article": "Value of Information and When to Wait",
        "decision_context": "",
        "decision_owner": "",
        "current_best_action": "",
        "information_options": [],
        "critical_uncertainties": [],
        "evidence_to_action_rules": [],
        "evpi": None,
        "evsi": None,
        "information_cost": None,
        "delay_cost": None,
        "net_value_information": None,
        "net_value_waiting": None,
        "decision_change_probability": None,
        "timing_recommendation": "",
        "stopping_rule": "",
        "stakeholder_delay_risks": [],
        "review_triggers": [],
        "post_decision_learning": []
    }
    path = RECORDS / "value_of_information_decision_record_template.json"
    path.write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()
