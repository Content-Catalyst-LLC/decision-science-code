#!/usr/bin/env python3
"""Decision record exporter for Bayesian decision-making."""

from __future__ import annotations

from pathlib import Path
import json

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
RECORDS = ARTICLE_ROOT / "outputs" / "decision_records"


def main() -> None:
    RECORDS.mkdir(parents=True, exist_ok=True)
    record = {
        "article": "Bayesian Decision-Making",
        "decision_context": "",
        "hypotheses": [],
        "prior_assumptions": [],
        "evidence": [],
        "likelihood_assumptions": [],
        "posterior_updates": [],
        "posterior_expected_utility": [],
        "prior_sensitivity": [],
        "likelihood_sensitivity": [],
        "value_of_information": [],
        "selected_action": "",
        "rationale": "",
        "review_triggers": [],
        "limitations": [],
    }
    path = RECORDS / "bayesian_decision_record_template.json"
    path.write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()
