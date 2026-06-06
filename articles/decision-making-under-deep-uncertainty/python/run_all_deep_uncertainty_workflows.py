#!/usr/bin/env python3
"""Run all Python workflows for Decision-Making Under Deep Uncertainty."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIR = ARTICLE_ROOT / "python"

SCRIPTS = [
    "ambiguity_profile_model.py",
    "exploratory_scenario_scan.py",
    "regret_analysis.py",
    "threshold_compliance.py",
    "vulnerability_analysis.py",
    "adaptive_strategy_simulation.py",
    "decision_record_exporter.py",
    "decision_making_under_deep_uncertainty_simulation.py",
]


def main() -> None:
    for script in SCRIPTS:
        path = PYTHON_DIR / script
        print(f"Running {path.name}...")
        subprocess.run([sys.executable, str(path)], check=True)
    print("All Python deep uncertainty workflows completed.")


if __name__ == "__main__":
    main()
