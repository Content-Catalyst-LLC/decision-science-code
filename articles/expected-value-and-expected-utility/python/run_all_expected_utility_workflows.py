#!/usr/bin/env python3
"""Run all Python workflows for Expected Value and Expected Utility."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIR = ARTICLE_ROOT / "python"

SCRIPTS = [
    "expected_value_calculator.py",
    "utility_function_profiles.py",
    "certainty_equivalent_calculator.py",
    "risk_premium_analysis.py",
    "risk_aversion_sensitivity.py",
    "probability_quality_audit.py",
    "decision_record_exporter.py",
    "expected_value_expected_utility_simulation.py",
]


def main() -> None:
    for script in SCRIPTS:
        path = PYTHON_DIR / script
        print(f"Running {path.name}...")
        subprocess.run([sys.executable, str(path)], check=True)
    print("All Python expected-utility workflows completed.")


if __name__ == "__main__":
    main()
