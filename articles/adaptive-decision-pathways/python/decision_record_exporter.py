#!/usr/bin/env python3
"""Decision record exporter for Adaptive Decision Pathways."""

from __future__ import annotations

from pathlib import Path
import json

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
RECORDS = ARTICLE_ROOT / "outputs" / "decision_records"


def main() -> None:
    RECORDS.mkdir(parents=True, exist_ok=True)
    record = {
        "article": "Adaptive Decision Pathways",
        "decision_context": "",
        "decision_owner": "",
        "system_boundary": "",
        "time_horizon": "",
        "stakeholders": [],
        "key_uncertainties": [],
        "initial_action": "",
        "future_options": [],
        "monitoring_indicators": [],
        "trigger_points": [],
        "switching_rules": [],
        "fallback_options": [],
        "scenario_tests": [],
        "option_value_considerations": [],
        "switching_costs": [],
        "governance_roles": {
            "indicator_owner": "",
            "trigger_authority": "",
            "switching_authority": "",
            "review_owner": ""
        },
        "stakeholder_review_points": [],
        "selected_pathway": "",
        "rationale": "",
        "dissent_or_contested_assumptions": [],
        "revision_history": []
    }
    path = RECORDS / "adaptive_decision_pathway_record_template.json"
    path.write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()
