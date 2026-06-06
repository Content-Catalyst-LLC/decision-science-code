#!/usr/bin/env python3
"""Decision record exporter for scenario evaluation and strategic choice."""

from __future__ import annotations

from pathlib import Path
import json

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
RECORDS = ARTICLE_ROOT / "outputs" / "decision_records"


def main() -> None:
    RECORDS.mkdir(parents=True, exist_ok=True)
    record = {
        "article": "Scenario Evaluation and Strategic Choice",
        "decision_context": "",
        "decision_owner": "",
        "decision_question": "",
        "time_horizon": "",
        "stakeholders": [],
        "scenario_purpose": "",
        "uncertainty_register": [],
        "excluded_uncertainties": [],
        "scenario_set": [],
        "strategy_set": [],
        "evaluation_criteria": [],
        "decision_rules": [],
        "thresholds": [],
        "scenario_performance": [],
        "regret_analysis": [],
        "vulnerability_conditions": [],
        "selected_strategy": "",
        "rationale": "",
        "dissent_or_contested_assumptions": [],
        "monitoring_indicators": [],
        "trigger_points": [],
        "fallback_options": [],
        "revision_authority": "",
        "post_decision_learning": []
    }
    path = RECORDS / "scenario_evaluation_decision_record_template.json"
    path.write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()
