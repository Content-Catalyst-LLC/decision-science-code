#!/usr/bin/env python3
"""Run all Python workflows for Decision Science in Public Policy."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIR = ARTICLE_ROOT / "python"

SCRIPTS = [
    "policy_value_model.py",
    "equity_review_model.py",
    "implementation_drift_model.py",
    "robustness_review_model.py",
    "policy_package_comparison.py",
    "decision_record_exporter.py",
    "decision_science_public_policy_simulation.py",
]


def main() -> None:
    for script in SCRIPTS:
        path = PYTHON_DIR / script
        print(f"Running {path.name}...")
        subprocess.run([sys.executable, str(path)], check=True)
    print("All Python public-policy workflows completed.")


if __name__ == "__main__":
    main()
