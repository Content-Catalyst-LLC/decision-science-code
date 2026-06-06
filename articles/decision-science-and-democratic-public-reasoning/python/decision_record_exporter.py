#!/usr/bin/env python3
"""Decision record exporter for Decision Science and Democratic Public Reasoning."""

from __future__ import annotations

from pathlib import Path
import json

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
RECORDS = ARTICLE_ROOT / "outputs" / "decision_records"


def main() -> None:
    RECORDS.mkdir(parents=True, exist_ok=True)
    record = {
        "article": "Decision Science and Democratic Public Reasoning",
        "decision_context": "",
        "public_authority": "",
        "decision_owner": "",
        "affected_publics": [],
        "stakeholder_standing": [],
        "public_purpose": "",
        "alternatives_considered": [],
        "excluded_alternatives": [],
        "criteria_and_values": [],
        "evidence_record": [],
        "model_or_metric_use": [],
        "assumptions": [],
        "uncertainties": [],
        "trade_offs": [],
        "participation_process": [],
        "public_input_summary": [],
        "response_to_public_input": [],
        "dissent_or_objections": [],
        "equity_review": [],
        "contestability_pathway": [],
        "selected_action": "",
        "public_rationale": "",
        "implementation_owner": "",
        "monitoring_indicators": [],
        "review_triggers": [],
        "correction_or_remedy_pathway": [],
        "revision_history": []
    }
    path = RECORDS / "democratic_public_reasoning_record_template.json"
    path.write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()
