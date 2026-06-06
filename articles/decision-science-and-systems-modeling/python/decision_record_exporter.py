#!/usr/bin/env python3
"""Decision record exporter for decision science and systems modeling."""

from __future__ import annotations

from pathlib import Path
import json

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
RECORDS = ARTICLE_ROOT / "outputs" / "decision_records"


def main() -> None:
    RECORDS.mkdir(parents=True, exist_ok=True)
    record = {
        "article": "Decision Science and Systems Modeling",
        "decision_context": "",
        "decision_owner": "",
        "model_purpose": "",
        "system_boundary": "",
        "included_elements": [],
        "excluded_elements": [],
        "state_variables": [],
        "stocks": [],
        "flows": [],
        "feedback_loops": [],
        "delays": [],
        "thresholds": [],
        "decision_interventions": [],
        "scenarios": [],
        "sensitivity_tests": [],
        "selected_strategy": "",
        "model_limitations": [],
        "monitoring_indicators": [],
        "revision_triggers": [],
        "rationale": "",
        "post_decision_learning": []
    }
    path = RECORDS / "systems_modeling_decision_record_template.json"
    path.write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()
