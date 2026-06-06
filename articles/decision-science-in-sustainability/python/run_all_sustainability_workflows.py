#!/usr/bin/env python3
"""Run all Python workflows for Decision Science in Sustainability."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIR = ARTICLE_ROOT / "python"

SCRIPTS = [
    "sustainability_value_model.py",
    "threshold_review_model.py",
    "resource_pressure_model.py",
    "equity_review_model.py",
    "sustainability_strategy_comparison.py",
    "decision_record_exporter.py",
    "decision_science_sustainability_simulation.py",
]


def main() -> None:
    for script in SCRIPTS:
        path = PYTHON_DIR / script
        print(f"Running {path.name}...")
        subprocess.run([sys.executable, str(path)], check=True)
    print("All Python sustainability workflows completed.")


if __name__ == "__main__":
    main()
