#!/usr/bin/env python3
"""Decision record exporter for framing effects in decision-making."""

from __future__ import annotations

from pathlib import Path
import json

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
RECORDS = ARTICLE_ROOT / "outputs" / "decision_records"


def main() -> None:
    RECORDS.mkdir(parents=True, exist_ok=True)
    record = {
        "article": "Framing Effects in Decision-Making",
        "decision_context": "",
        "current_frame": "",
        "equivalent_frames_tested": [],
        "reference_points": [],
        "gain_frame_choice": "",
        "loss_frame_choice": "",
        "frame_reversal": None,
        "absolute_risk_format": "",
        "relative_risk_format": "",
        "values_emphasized": [],
        "values_hidden": [],
        "stakeholder_frame_concerns": [],
        "selected_action": "",
        "rationale": "",
        "review_triggers": [],
        "post_decision_learning": [],
    }
    path = RECORDS / "framing_effects_decision_record_template.json"
    path.write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()
