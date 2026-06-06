#!/usr/bin/env python3
"""Run all Python workflows for Stakeholder Values and Decision Legitimacy."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIR = ARTICLE_ROOT / "python"

SCRIPTS = [
    "stakeholder_mapping.py",
    "value_weight_model.py",
    "burden_analysis.py",
    "procedural_legitimacy.py",
    "threshold_checks.py",
    "legitimacy_index.py",
    "decision_record_exporter.py",
    "stakeholder_values_decision_legitimacy_simulation.py",
]


def main() -> None:
    for script in SCRIPTS:
        path = PYTHON_DIR / script
        print(f"Running {path.name}...")
        subprocess.run([sys.executable, str(path)], check=True)
    print("All Python stakeholder legitimacy workflows completed.")


if __name__ == "__main__":
    main()
