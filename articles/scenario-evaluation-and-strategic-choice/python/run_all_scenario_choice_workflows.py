#!/usr/bin/env python3
"""Run all Python workflows for Scenario Evaluation and Strategic Choice."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIR = ARTICLE_ROOT / "python"

SCRIPTS = [
    "expected_value_model.py",
    "maximin_model.py",
    "minimax_regret_model.py",
    "threshold_pass_rate_model.py",
    "scenario_dispersion_model.py",
    "scenario_strategy_comparison.py",
    "decision_record_exporter.py",
    "scenario_evaluation_strategic_choice_simulation.py",
]


def main() -> None:
    for script in SCRIPTS:
        path = PYTHON_DIR / script
        print(f"Running {path.name}...")
        subprocess.run([sys.executable, str(path)], check=True)
    print("All Python scenario-choice workflows completed.")


if __name__ == "__main__":
    main()
