#!/usr/bin/env python3
"""Decision record exporter for path dependence, lock-in, and decision timing."""

from __future__ import annotations

from pathlib import Path
import json

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
RECORDS = ARTICLE_ROOT / "outputs" / "decision_records"


def main() -> None:
    RECORDS.mkdir(parents=True, exist_ok=True)
    record = {
        "article": "Path Dependence, Lock-In, and Decision Timing",
        "decision_context": "",
        "decision_owner": "",
        "current_path": "",
        "alternative_paths": [],
        "time_horizon": "",
        "historical_commitments": [],
        "lock_in_mechanisms": {
            "technical": [],
            "economic": [],
            "institutional": [],
            "behavioral": [],
            "political": [],
            "infrastructure": [],
            "legal_or_contractual": []
        },
        "sunk_costs": [],
        "switching_costs": [],
        "option_value_considerations": [],
        "timing_logic": "",
        "strategic_windows": [],
        "scenario_tests": [],
        "exit_paths": [],
        "transition_plan": [],
        "stakeholder_burdens": [],
        "review_triggers": [],
        "selected_path": "",
        "rationale": "",
        "dissent_or_contested_assumptions": [],
        "revision_authority": "",
        "post_decision_learning": []
    }
    path = RECORDS / "path_dependence_decision_record_template.json"
    path.write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()
