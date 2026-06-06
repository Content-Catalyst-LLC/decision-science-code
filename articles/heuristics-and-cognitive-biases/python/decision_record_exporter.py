#!/usr/bin/env python3
"""Decision record exporter for heuristics and cognitive biases."""

from __future__ import annotations

from pathlib import Path
import json

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
RECORDS = ARTICLE_ROOT / "outputs" / "decision_records"


def main() -> None:
    RECORDS.mkdir(parents=True, exist_ok=True)
    record = {
        "article": "Heuristics and Cognitive Biases",
        "decision_context": "",
        "decision_frame": "",
        "alternatives": [],
        "base_rates": [],
        "independent_estimates": [],
        "bias_risks": [],
        "judged_probability": None,
        "confidence": None,
        "confidence_gap": None,
        "calibration_notes": "",
        "disconfirming_evidence": [],
        "premortem_findings": [],
        "dissent": [],
        "selected_action": "",
        "review_triggers": [],
        "post_decision_learning": [],
    }
    path = RECORDS / "heuristics_cognitive_biases_decision_record_template.json"
    path.write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()
