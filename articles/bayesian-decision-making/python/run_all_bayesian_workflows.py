#!/usr/bin/env python3
"""Run all Python workflows for Bayesian Decision-Making."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIR = ARTICLE_ROOT / "python"

SCRIPTS = [
    "bayes_update_calculator.py",
    "posterior_odds_bayes_factor.py",
    "posterior_expected_utility.py",
    "prior_sensitivity_analysis.py",
    "sequential_learning_simulation.py",
    "value_of_information_analysis.py",
    "evidence_quality_audit.py",
    "decision_record_exporter.py",
    "bayesian_decision_making_simulation.py",
]


def main() -> None:
    for script in SCRIPTS:
        path = PYTHON_DIR / script
        print(f"Running {path.name}...")
        subprocess.run([sys.executable, str(path)], check=True)
    print("All Python Bayesian workflows completed.")


if __name__ == "__main__":
    main()
