#!/usr/bin/env python3
"""Decision record exporter for judgment under uncertainty."""

from __future__ import annotations

from pathlib import Path
import json

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
RECORDS = ARTICLE_ROOT / "outputs" / "decision_records"


def main() -> None:
    RECORDS.mkdir(parents=True, exist_ok=True)
    record = {
        "article": "Judgment Under Uncertainty",
        "decision_context": "",
        "judgment_target": "",
        "prior_probability": None,
        "reference_class": "",
        "evidence": [],
        "likelihood_if_true": None,
        "likelihood_if_false": None,
        "posterior_probability": None,
        "forecast_probability": None,
        "confidence": None,
        "confidence_rationale": "",
        "competing_hypotheses": [],
        "bias_checks": {
            "base_rate_neglect": "",
            "anchoring": "",
            "availability": "",
            "confirmation_bias": "",
            "overconfidence": "",
            "framing_effects": ""
        },
        "action_threshold": "",
        "selected_action": "",
        "review_triggers": [],
        "post_decision_learning": []
    }
    path = RECORDS / "judgment_under_uncertainty_decision_record_template.json"
    path.write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()
