#!/usr/bin/env python3
"""Run all Python workflows for Decision Science in Healthcare."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIR = ARTICLE_ROOT / "python"

SCRIPTS = [
    "treatment_value_model.py",
    "diagnostic_probability_model.py",
    "cost_effectiveness_model.py",
    "capacity_queue_model.py",
    "healthcare_strategy_comparison.py",
    "decision_record_exporter.py",
    "decision_science_healthcare_simulation.py",
]


def main() -> None:
    for script in SCRIPTS:
        path = PYTHON_DIR / script
        print(f"Running {path.name}...")
        subprocess.run([sys.executable, str(path)], check=True)
    print("All Python healthcare workflows completed.")


if __name__ == "__main__":
    main()
