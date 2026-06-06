#!/usr/bin/env python3
"""Decision record exporter for Decision Science in Organizational Strategy."""

from __future__ import annotations

from pathlib import Path
import json

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
RECORDS = ARTICLE_ROOT / "outputs" / "decision_records"


def main() -> None:
    RECORDS.mkdir(parents=True, exist_ok=True)
    record = {
        "article": "Decision Science in Organizational Strategy",
        "decision_context": "",
        "decision_owner": "",
        "strategic_decision_type": "",
        "time_horizon": "",
        "strategic_question": "",
        "uncertainty_regime": "",
        "strategic_options": [],
        "selected_option": "",
        "assumptions": [],
        "evidence_base": [],
        "scenario_results": [],
        "resource_commitments": [],
        "capability_requirements": [],
        "capability_gaps": [],
        "governance_conditions": [],
        "incentive_risks": [],
        "behavioral_risks": [],
        "systems_effects": [],
        "tradeoffs": [],
        "dissent_or_challenge_notes": [],
        "decision_rationale": "",
        "approval_authority": "",
        "leading_indicators": [],
        "review_triggers": [],
        "exit_criteria": [],
        "revision_history": []
    }
    path = RECORDS / "organizational_strategy_decision_record_template.json"
    path.write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()
