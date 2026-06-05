#!/usr/bin/env python3
"""Run all Python workflows for Why Uncertainty Changes Decision-Making."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIR = ARTICLE_ROOT / "python"

SCRIPTS = [
    "expected_utility_under_risk.py",
    "ambiguity_adjusted_choice.py",
    "minimax_regret_uncertainty.py",
    "robustness_threshold_diagnostics.py",
    "adaptive_pathway_simulation.py",
    "value_of_information_estimator.py",
    "uncertainty_decision_record_exporter.py",
    "why_uncertainty_changes_decision_making_simulation.py",
]


def main() -> None:
    for script in SCRIPTS:
        path = PYTHON_DIR / script
        print(f"Running {path.name}...")
        subprocess.run([sys.executable, str(path)], check=True)
    print("All Python uncertainty workflows completed.")


if __name__ == "__main__":
    main()
