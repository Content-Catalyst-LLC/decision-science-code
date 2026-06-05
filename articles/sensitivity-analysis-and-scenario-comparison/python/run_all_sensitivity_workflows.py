#!/usr/bin/env python3
"""Run all Python workflows for Sensitivity Analysis and Scenario Comparison."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIR = ARTICLE_ROOT / "python"

SCRIPTS = [
    "one_way_sensitivity.py",
    "multi_way_sensitivity.py",
    "threshold_analysis.py",
    "scenario_robustness_profiles.py",
    "regret_analysis.py",
    "probabilistic_sensitivity.py",
    "key_driver_diagnostics.py",
    "decision_record_exporter.py",
    "sensitivity_analysis_scenario_comparison_simulation.py",
]


def main() -> None:
    for script in SCRIPTS:
        path = PYTHON_DIR / script
        print(f"Running {path.name}...")
        subprocess.run([sys.executable, str(path)], check=True)
    print("All Python sensitivity-analysis workflows completed.")


if __name__ == "__main__":
    main()
