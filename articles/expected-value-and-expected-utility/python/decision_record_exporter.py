#!/usr/bin/env python3
"""Decision record exporter for expected value and expected utility."""

from __future__ import annotations

from pathlib import Path
import json

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
RECORDS = ARTICLE_ROOT / "outputs" / "decision_records"


def main() -> None:
    RECORDS.mkdir(parents=True, exist_ok=True)
    record = {
        "article": "Expected Value and Expected Utility",
        "decision_context": "",
        "alternatives": [],
        "outcome_states": [],
        "probabilities": [],
        "probability_sources": [],
        "expected_value_results": [],
        "utility_function": "",
        "risk_aversion_parameter": None,
        "expected_utility_results": [],
        "certainty_equivalents": [],
        "risk_premiums": [],
        "sensitivity_results": [],
        "selected_action": "",
        "rationale": "",
        "limitations": [],
        "review_triggers": [],
    }
    path = RECORDS / "expected_utility_decision_record_template.json"
    path.write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()
