#!/usr/bin/env python3
"""Decision record exporter for behavioral decision theory."""

from __future__ import annotations

from pathlib import Path
import json

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
RECORDS = ARTICLE_ROOT / "outputs" / "decision_records"


def main() -> None:
    RECORDS.mkdir(parents=True, exist_ok=True)
    record = {
        "article": "Behavioral Decision Theory",
        "decision_context": "",
        "formal_benchmark": "",
        "alternatives": [],
        "reference_points": [],
        "frames_tested": [],
        "expected_utility_results": [],
        "prospect_theory_results": [],
        "probability_weighting_notes": [],
        "loss_aversion_notes": [],
        "rank_divergence": None,
        "behavioral_review_flags": [],
        "choice_architecture_review": {
            "defaults": "",
            "labels": "",
            "option_order": "",
            "visual_emphasis": "",
            "comparison_set": ""
        },
        "dissent": [],
        "selected_action": "",
        "rationale": "",
        "review_triggers": [],
        "post_decision_learning": []
    }
    path = RECORDS / "behavioral_decision_theory_decision_record_template.json"
    path.write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()
