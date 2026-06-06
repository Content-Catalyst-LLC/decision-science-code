#!/usr/bin/env python3
"""Run all Python workflows for Multi-Criteria Decision Analysis."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIR = ARTICLE_ROOT / "python"

SCRIPTS = [
    "weighted_score_model.py",
    "criteria_normalization.py",
    "rank_stability_analysis.py",
    "stakeholder_weight_profiles.py",
    "outranking_review.py",
    "mcda_review_queue.py",
    "decision_record_exporter.py",
    "mcda_weight_sensitivity_simulation.py",
]


def main() -> None:
    for script in SCRIPTS:
        path = PYTHON_DIR / script
        print(f"Running {path.name}...")
        subprocess.run([sys.executable, str(path)], check=True)
    print("All Python MCDA workflows completed.")


if __name__ == "__main__":
    main()
