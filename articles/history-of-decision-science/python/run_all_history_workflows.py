#!/usr/bin/env python3
"""Run all Python workflows for The History of Decision Science."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIR = ARTICLE_ROOT / "python"

SCRIPTS = [
    "expected_value_historical_baseline.py",
    "expected_utility_bernoulli_model.py",
    "subjective_probability_savage_model.py",
    "bayesian_update_history_example.py",
    "bounded_rationality_satisficing.py",
    "behavioral_noise_choice_model.py",
    "minimax_regret_history.py",
    "robustness_historical_paradigms.py",
    "decision_record_exporter.py",
    "history_of_decision_science_simulation.py",
]


def main() -> None:
    for script in SCRIPTS:
        path = PYTHON_DIR / script
        print(f"Running {path.name}...")
        subprocess.run([sys.executable, str(path)], check=True)
    print("All Python history workflows completed.")


if __name__ == "__main__":
    main()
