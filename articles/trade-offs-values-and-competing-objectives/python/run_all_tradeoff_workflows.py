#!/usr/bin/env python3
"""Run all Python workflows for Trade-Offs, Values, and Competing Objectives."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIR = ARTICLE_ROOT / "python"

SCRIPTS = [
    "weighted_objective_model.py",
    "dominance_analysis.py",
    "rank_stability_analysis.py",
    "scenario_regret_analysis.py",
    "stakeholder_value_profiles.py",
    "tradeoff_review_queue.py",
    "decision_record_exporter.py",
    "tradeoffs_values_competing_objectives_simulation.py",
]


def main() -> None:
    for script in SCRIPTS:
        path = PYTHON_DIR / script
        print(f"Running {path.name}...")
        subprocess.run([sys.executable, str(path)], check=True)
    print("All Python trade-off workflows completed.")


if __name__ == "__main__":
    main()
