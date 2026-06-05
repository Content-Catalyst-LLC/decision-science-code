#!/usr/bin/env python3
"""Decision record exporter template."""

from __future__ import annotations

from pathlib import Path
import json

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
RECORDS = ARTICLE_ROOT / "outputs" / "decision_records"


def main() -> None:
    RECORDS.mkdir(parents=True, exist_ok=True)
    record = {
        "article": "Core Principles of Decision Science",
        "decision_frame": "",
        "decision_owner": "",
        "alternatives": [],
        "criteria": [],
        "weights": {},
        "assumptions": [],
        "evidence": [],
        "uncertainties": [],
        "tradeoffs": [],
        "behavioral_safeguards": [],
        "systems_consequences": [],
        "selected_action": "",
        "rationale": "",
        "review_triggers": [],
        "monitoring_indicators": [],
    }
    path = RECORDS / "core_principles_decision_record_template.json"
    path.write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()
