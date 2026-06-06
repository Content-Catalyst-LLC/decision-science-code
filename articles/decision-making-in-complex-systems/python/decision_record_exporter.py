#!/usr/bin/env python3
"""Decision record exporter for complex-system decisions."""

from __future__ import annotations

from pathlib import Path
import json

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
RECORDS = ARTICLE_ROOT / "outputs" / "decision_records"


def main() -> None:
    RECORDS.mkdir(parents=True, exist_ok=True)
    record = {
        "article": "Decision-Making in Complex Systems",
        "decision_context": "",
        "decision_owner": "",
        "system_boundary": "",
        "key_components": [],
        "interdependencies": [],
        "feedback_loops": [],
        "delays": [],
        "thresholds": [],
        "adaptation_risks": [],
        "scenarios": [],
        "strategy_options": [],
        "selected_strategy": "",
        "rationale": "",
        "monitoring_indicators": [],
        "trigger_points": [],
        "fallback_options": [],
        "dissent_or_contested_assumptions": [],
        "post_decision_learning": []
    }
    path = RECORDS / "complex_system_decision_record_template.json"
    path.write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()
