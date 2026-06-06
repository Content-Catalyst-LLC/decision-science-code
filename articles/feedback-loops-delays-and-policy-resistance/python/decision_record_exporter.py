#!/usr/bin/env python3
"""Decision record exporter for feedback loops, delays, and policy resistance."""

from __future__ import annotations

from pathlib import Path
import json

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
RECORDS = ARTICLE_ROOT / "outputs" / "decision_records"


def main() -> None:
    RECORDS.mkdir(parents=True, exist_ok=True)
    record = {
        "article": "Feedback Loops, Delays, and Policy Resistance",
        "decision_context": "",
        "decision_owner": "",
        "policy_problem": "",
        "target_outcome": "",
        "system_boundary": "",
        "recurring_pattern": "",
        "stocks": [],
        "flows": [],
        "reinforcing_loops": [],
        "balancing_loops": [],
        "implementation_delays": [],
        "outcome_delays": [],
        "recognition_delays": [],
        "policy_resistance_pathways": [],
        "unintended_consequence_risks": [],
        "scenarios": [],
        "monitoring_indicators": [],
        "review_triggers": [],
        "selected_policy": "",
        "rationale": "",
        "dissent_or_contested_assumptions": [],
        "revision_authority": "",
        "post_decision_learning": []
    }
    path = RECORDS / "feedback_delay_policy_decision_record_template.json"
    path.write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()
