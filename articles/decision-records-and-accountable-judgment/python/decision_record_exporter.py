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
        "article": "Decision Records and Accountable Judgment",
        "decision_statement": "",
        "decision_owner": "",
        "recommendation_owner": "",
        "decision_date": "",
        "context": "",
        "alternatives_considered": [],
        "alternatives_rejected_or_deferred": [],
        "evidence_claim_links": [],
        "assumptions": [],
        "uncertainties": [],
        "criteria": [],
        "tradeoffs": [],
        "dissent": [],
        "selected_action": "",
        "rationale": "",
        "implementation_owner": "",
        "monitoring_indicators": [],
        "review_triggers": [],
        "revision_authority": "",
    }
    path = RECORDS / "decision_record_blank_template.json"
    path.write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()
