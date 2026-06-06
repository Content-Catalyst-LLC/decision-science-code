#!/usr/bin/env python3
from pathlib import Path
import json

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
RECORDS = ARTICLE_ROOT / "outputs" / "decision_records"

def main() -> None:
    RECORDS.mkdir(parents=True, exist_ok=True)
    record = {
        "article": "Decision Science in Crisis Management",
        "decision_context": "",
        "decision_owner": "",
        "crisis_type": "",
        "decision_required_now": "",
        "confirmed_facts": [],
        "working_assumptions": [],
        "unknowns": [],
        "confidence_level": "",
        "response_priorities": [],
        "affected_populations": [],
        "response_options": [],
        "selected_action": "",
        "rationale": "",
        "authority": "",
        "resource_constraints": [],
        "communication_plan": [],
        "equity_and_ethics_review": [],
        "cascading_risks": [],
        "monitoring_indicators": [],
        "escalation_triggers": [],
        "after_action_questions": [],
        "revision_history": []
    }
    path = RECORDS / "crisis_management_decision_record_template.json"
    path.write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(path)

if __name__ == "__main__":
    main()
