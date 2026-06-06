#!/usr/bin/env python3
"""Run all Python workflows for Decision Science in Organizational Strategy."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIR = ARTICLE_ROOT / "python"

SCRIPTS = [
    "strategic_option_model.py",
    "robustness_model.py",
    "assumption_drift_model.py",
    "capability_fit_model.py",
    "organizational_strategy_comparison.py",
    "decision_record_exporter.py",
    "decision_science_organizational_strategy_simulation.py",
]


def main() -> None:
    for script in SCRIPTS:
        path = PYTHON_DIR / script
        print(f"Running {path.name}...")
        subprocess.run([sys.executable, str(path)], check=True)
    print("All Python organizational-strategy workflows completed.")


if __name__ == "__main__":
    main()
