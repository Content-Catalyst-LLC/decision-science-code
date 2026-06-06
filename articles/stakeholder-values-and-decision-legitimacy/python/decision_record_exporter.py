#!/usr/bin/env python3
"""Decision record exporter for stakeholder values and decision legitimacy."""

from __future__ import annotations

from pathlib import Path
import json

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
RECORDS = ARTICLE_ROOT / "outputs" / "decision_records"


def main() -> None:
    RECORDS.mkdir(parents=True, exist_ok=True)
    record = {
        "article": "Stakeholder Values and Decision Legitimacy",
        "decision_context": "",
        "decision_owner": "",
        "stakeholder_map": [],
        "affectedness_analysis": [],
        "value_criteria": [],
        "stakeholder_value_weights": [],
        "alternatives": [],
        "burden_analysis": [],
        "procedural_legitimacy_review": {
            "voice": None,
            "transparency": None,
            "explanation": None,
            "contestability": None,
            "review": None
        },
        "thresholds": [],
        "dissent_or_contested_assumptions": [],
        "selected_action": "",
        "rationale": "",
        "mitigation_requirements": [],
        "monitoring_triggers": [],
        "review_authority": "",
        "post_decision_learning": []
    }
    path = RECORDS / "stakeholder_values_decision_record_template.json"
    path.write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()
