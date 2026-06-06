#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
RECORDS = ROOT / "outputs" / "decision_records"

def main():
    RECORDS.mkdir(parents=True, exist_ok=True)
    record = {
        "article": "Ethics of Decision Science",
        "decision_context": "",
        "decision_authority": "",
        "moral_stakes": [],
        "values_and_criteria": [],
        "non_tradeable_constraints": [],
        "alternatives_considered": [],
        "stakeholders": [],
        "evidence": [],
        "assumptions": [],
        "uncertainties": [],
        "distributional_analysis": [],
        "transparency_plan": [],
        "contestability_mechanism": [],
        "dissent_or_challenge_notes": [],
        "selected_action": "",
        "rationale": "",
        "review_triggers": [],
        "remedy_or_correction_pathways": [],
        "revision_history": []
    }
    path = RECORDS / "ethical_decision_record_template.json"
    path.write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(path)

if __name__ == "__main__":
    main()
