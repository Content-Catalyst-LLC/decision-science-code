#!/usr/bin/env python3
"""Decision record exporter for group decision-making and social influence."""

from __future__ import annotations

from pathlib import Path
import json

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
RECORDS = ARTICLE_ROOT / "outputs" / "decision_records"


def main() -> None:
    RECORDS.mkdir(parents=True, exist_ok=True)
    record = {
        "article": "Group Decision-Making and Social Influence",
        "decision_context": "",
        "decision_owner": "",
        "decision_rule": "",
        "participants": [],
        "independent_judgments": [],
        "shared_evidence": [],
        "unique_evidence": [],
        "dissent": [],
        "influence_risks": {
            "authority_anchoring": "",
            "conformity_pressure": "",
            "status_weighting": "",
            "hidden_profile_risk": ""
        },
        "alternatives_considered": [],
        "selected_action": "",
        "rationale": "",
        "review_triggers": [],
        "post_decision_learning": []
    }
    path = RECORDS / "group_decision_record_template.json"
    path.write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()
