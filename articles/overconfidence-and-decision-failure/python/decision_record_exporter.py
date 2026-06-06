#!/usr/bin/env python3
"""Decision record exporter for overconfidence and decision failure."""

from __future__ import annotations

from pathlib import Path
import json

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
RECORDS = ARTICLE_ROOT / "outputs" / "decision_records"


def main() -> None:
    RECORDS.mkdir(parents=True, exist_ok=True)
    record = {
        "article": "Overconfidence and Decision Failure",
        "decision_context": "",
        "decision_owner": "",
        "confidence_claims": [],
        "forecast_probabilities": [],
        "uncertainty_ranges": [],
        "reference_classes": [],
        "assumptions": [],
        "disconfirming_evidence": [],
        "dissent": [],
        "model_outputs_used": [],
        "model_limitations": [],
        "planning_estimates": {
            "estimated_duration": None,
            "estimated_cost": None,
            "confidence_interval": ""
        },
        "selected_action": "",
        "rationale": "",
        "review_triggers": [],
        "post_decision_learning": []
    }
    path = RECORDS / "overconfidence_decision_record_template.json"
    path.write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()
