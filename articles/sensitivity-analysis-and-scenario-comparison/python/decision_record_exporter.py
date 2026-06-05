#!/usr/bin/env python3
"""Decision record exporter for sensitivity analysis and scenario comparison."""

from __future__ import annotations

from pathlib import Path
import json

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
RECORDS = ARTICLE_ROOT / "outputs" / "decision_records"


def main() -> None:
    RECORDS.mkdir(parents=True, exist_ok=True)
    record = {
        "article": "Sensitivity Analysis and Scenario Comparison",
        "decision_context": "",
        "alternatives": [],
        "baseline_assumptions": [],
        "uncertain_inputs": [],
        "input_ranges": [],
        "scenarios": [],
        "one_way_sensitivity": [],
        "multi_way_sensitivity": [],
        "thresholds": [],
        "ranking_stability": [],
        "robustness_results": [],
        "regret_results": [],
        "probabilistic_sensitivity": [],
        "key_drivers": [],
        "selected_strategy": "",
        "rationale": "",
        "review_triggers": [],
        "limitations": [],
    }
    path = RECORDS / "sensitivity_scenario_decision_record_template.json"
    path.write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()
