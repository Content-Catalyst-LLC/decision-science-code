#!/usr/bin/env python3
"""Decision record exporter for Decision Science in Sustainability."""

from __future__ import annotations

from pathlib import Path
import json

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
RECORDS = ARTICLE_ROOT / "outputs" / "decision_records"


def main() -> None:
    RECORDS.mkdir(parents=True, exist_ok=True)
    record = {
        "article": "Decision Science in Sustainability",
        "decision_context": "",
        "decision_owner": "",
        "system_boundary": "",
        "time_horizon": "",
        "affected_ecosystems": [],
        "affected_populations": [],
        "stakeholders": [],
        "objectives": {
            "environmental": "",
            "social": "",
            "economic": "",
            "governance": "",
            "resilience": "",
            "justice": ""
        },
        "ecological_thresholds": [],
        "safe_minimum_standards": [],
        "strategy_alternatives": [],
        "evidence_base": [],
        "uncertainties": [],
        "assumptions": [],
        "tradeoffs": [],
        "distributional_impacts": [],
        "systems_effects": [],
        "behavioral_considerations": [],
        "implementation_requirements": [],
        "monitoring_indicators": [],
        "trigger_points": [],
        "fallback_options": [],
        "selected_strategy": "",
        "rationale": "",
        "dissent_or_contested_assumptions": [],
        "revision_authority": "",
        "public_explanation": "",
        "review_history": []
    }
    path = RECORDS / "sustainability_decision_record_template.json"
    path.write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()
