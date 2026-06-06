#!/usr/bin/env python3
"""Decision record exporter for Decision Science in Financial Risk Management."""

from __future__ import annotations

from pathlib import Path
import json

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
RECORDS = ARTICLE_ROOT / "outputs" / "decision_records"


def main() -> None:
    RECORDS.mkdir(parents=True, exist_ok=True)
    record = {
        "article": "Decision Science in Financial Risk Management",
        "decision_context": "",
        "decision_owner": "",
        "decision_type": "",
        "portfolio_or_exposure": "",
        "time_horizon": "",
        "risk_appetite": "",
        "risk_capacity": "",
        "capital_constraints": [],
        "liquidity_constraints": [],
        "models_used": [],
        "model_limitations": [],
        "data_sources": [],
        "assumptions": [],
        "stress_scenarios": [],
        "scenario_results": [],
        "management_overlays": [],
        "alternatives_considered": [],
        "behavioral_or_incentive_risks": [],
        "governance_review": [],
        "dissent_or_challenge_notes": [],
        "selected_action": "",
        "rationale": "",
        "approval_authority": "",
        "monitoring_indicators": [],
        "trigger_points": [],
        "revision_history": []
    }
    path = RECORDS / "financial_risk_decision_record_template.json"
    path.write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()
