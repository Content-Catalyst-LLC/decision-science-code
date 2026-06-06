#!/usr/bin/env python3
"""Decision record exporter for decision hygiene and bias reduction."""

from __future__ import annotations

from pathlib import Path
import json

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
RECORDS = ARTICLE_ROOT / "outputs" / "decision_records"


def main() -> None:
    RECORDS.mkdir(parents=True, exist_ok=True)
    record = {
        "article": "Decision Hygiene and Bias Reduction",
        "decision_context": "",
        "decision_owner": "",
        "decision_rule": "",
        "bias_risks": [],
        "noise_risks": [],
        "evidence_inventory": [],
        "base_rates": [],
        "reference_classes": [],
        "independent_estimates": [],
        "framing_checks": [],
        "structured_dissent": [],
        "model_or_ai_review": {
            "model_used": "",
            "validation_status": "",
            "calibration_status": "",
            "known_limitations": ""
        },
        "confidence_estimates": [],
        "selected_action": "",
        "rationale": "",
        "review_triggers": [],
        "post_decision_learning": []
    }
    path = RECORDS / "decision_hygiene_record_template.json"
    path.write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()
