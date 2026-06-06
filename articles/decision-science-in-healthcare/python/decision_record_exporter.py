#!/usr/bin/env python3
"""Decision record exporter for Decision Science in Healthcare."""

from __future__ import annotations

from pathlib import Path
import json

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
RECORDS = ARTICLE_ROOT / "outputs" / "decision_records"


def main() -> None:
    RECORDS.mkdir(parents=True, exist_ok=True)
    record = {
        "article": "Decision Science in Healthcare",
        "decision_context": "",
        "decision_owner": "",
        "patient_or_population_context": "",
        "decision_type": "",
        "time_horizon": "",
        "clinical_evidence": [],
        "diagnostic_evidence": [],
        "uncertainties": [],
        "reasonable_options": [],
        "expected_benefits": [],
        "harms_and_adverse_events": [],
        "patient_values_and_preferences": [],
        "resource_constraints": [],
        "cost_effectiveness_considerations": [],
        "equity_considerations": [],
        "operational_constraints": [],
        "systems_effects": [],
        "ai_or_decision_support_role": "",
        "monitoring_indicators": [],
        "trigger_points": [],
        "escalation_rules": [],
        "selected_option": "",
        "rationale": "",
        "dissent_or_contested_assumptions": [],
        "follow_up_plan": "",
        "revision_history": []
    }
    path = RECORDS / "healthcare_decision_record_template.json"
    path.write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()
