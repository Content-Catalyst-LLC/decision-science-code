#!/usr/bin/env python3
"""Decision-record generator scaffold."""

from __future__ import annotations

from pathlib import Path
import json

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
RECORDS = ARTICLE_ROOT / "outputs" / "decision_records"


def write_record() -> Path:
    RECORDS.mkdir(parents=True, exist_ok=True)
    record = {
        "decision": "Template decision record",
        "alternatives_considered": [],
        "criteria": [],
        "assumptions": [],
        "evidence": [],
        "uncertainties": [],
        "rationale": "",
        "review_triggers": [],
    }
    path = RECORDS / "decision_record_template.json"
    path.write_text(json.dumps(record, indent=2), encoding="utf-8")
    return path


if __name__ == "__main__":
    print(write_record())
