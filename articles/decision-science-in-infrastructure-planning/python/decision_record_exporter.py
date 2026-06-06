#!/usr/bin/env python3
"""Decision record exporter for Decision Science in Infrastructure Planning."""

from __future__ import annotations

from pathlib import Path
import json

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
RECORDS = ARTICLE_ROOT / "outputs" / "decision_records"


def main() -> None:
    RECORDS.mkdir(parents=True, exist_ok=True)
    record = {
        "article": "Decision Science in Infrastructure Planning",
        "decision_context": "",
        "decision_owner": "",
        "public_need": "",
        "system_boundary": "",
        "time_horizon": "",
        "infrastructure_alternatives": [],
        "selected_alternative": "",
        "assumptions": [],
        "forecasts": [],
        "scenarios": [],
        "lifecycle_costs": [],
        "service_value": [],
        "equity_considerations": [],
        "environmental_considerations": [],
        "resilience_considerations": [],
        "interdependencies": [],
        "funding_and_financing": [],
        "governance_conditions": [],
        "procurement_risks": [],
        "community_engagement_notes": [],
        "tradeoffs": [],
        "dissent_or_challenge_notes": [],
        "selected_action_rationale": "",
        "monitoring_indicators": [],
        "adaptive_triggers": [],
        "revision_history": []
    }
    path = RECORDS / "infrastructure_decision_record_template.json"
    path.write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()
