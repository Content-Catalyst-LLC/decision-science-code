#!/usr/bin/env python3
"""Run all Python workflows for What Is Decision Science?"""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIR = ARTICLE_ROOT / "python"

SCRIPTS = [
    "validation_checks.py",
    "expected_value_utility_model.py",
    "decision_tree_diagnostics.py",
    "regret_analysis_minimax.py",
    "robustness_scenario_comparison.py",
    "sensitivity_threshold_analysis.py",
    "decision_record_generator.py",
    "decision_science_diagnostics_workflow.py",
]


def main() -> None:
    for script in SCRIPTS:
        path = PYTHON_DIR / script
        print(f"Running {path.name}...")
        subprocess.run([sys.executable, str(path)], check=True)
    print("All Python decision science workflows completed.")


if __name__ == "__main__":
    main()
