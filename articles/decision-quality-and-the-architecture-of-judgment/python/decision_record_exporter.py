#!/usr/bin/env python3
"""Decision record exporter template for decision-quality reviews."""

from __future__ import annotations

from pathlib import Path
import json

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
RECORDS = ARTICLE_ROOT / "outputs" / "decision_records"


def main() -> None:
    RECORDS.mkdir(parents=True, exist_ok=True)
    record = {
        "article": "Decision Quality and the Architecture of Judgment",
        "decision_context": "",
        "decision_owner": "",
        "alternatives": [],
        "evidence": [],
        "uncertainties": [],
        "criteria": [],
        "tradeoffs": [],
        "behavioral_safeguards": [],
        "systems_consequences": [],
        "selected_action": "",
        "rationale": "",
        "dissent": [],
        "monitoring_indicators": [],
        "review_triggers": [],
        "process_review": {
            "decision_quality_score": None,
            "outcome_quality": None,
            "outcome_bias_warning": "",
        },
    }
    path = RECORDS / "decision_quality_record_template.json"
    path.write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()
