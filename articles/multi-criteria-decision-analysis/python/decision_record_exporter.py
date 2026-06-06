#!/usr/bin/env python3
"""Decision record exporter for Multi-Criteria Decision Analysis."""

from __future__ import annotations

from pathlib import Path
import json

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
RECORDS = ARTICLE_ROOT / "outputs" / "decision_records"


def main() -> None:
    RECORDS.mkdir(parents=True, exist_ok=True)
    record = {
        "article": "Multi-Criteria Decision Analysis",
        "decision_context": "",
        "decision_owner": "",
        "decision_rule": "",
        "alternatives": [],
        "criteria": [],
        "criterion_directions": {},
        "score_sources": [],
        "normalization_method": "",
        "weights": {},
        "stakeholder_weight_profiles": [],
        "aggregation_method": "",
        "sensitivity_tests": [],
        "rank_stability": [],
        "dissent_or_disagreement": [],
        "selected_action": "",
        "rationale": "",
        "review_triggers": [],
        "post_decision_learning": []
    }
    path = RECORDS / "mcda_decision_record_template.json"
    path.write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()
