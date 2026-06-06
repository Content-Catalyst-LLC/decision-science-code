#!/usr/bin/env python3
"""Run all Python workflows for Value of Information and When to Wait."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIR = ARTICLE_ROOT / "python"

SCRIPTS = [
    "expected_value_model.py",
    "evpi_calculator.py",
    "evsi_calculator.py",
    "delay_cost_model.py",
    "decision_change_probability.py",
    "timing_recommendation.py",
    "decision_record_exporter.py",
    "value_of_information_when_to_wait_simulation.py",
]


def main() -> None:
    for script in SCRIPTS:
        path = PYTHON_DIR / script
        print(f"Running {path.name}...")
        subprocess.run([sys.executable, str(path)], check=True)
    print("All Python value-of-information workflows completed.")


if __name__ == "__main__":
    main()
