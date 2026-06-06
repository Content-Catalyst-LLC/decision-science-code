#!/usr/bin/env python3
"""Run all Python workflows for Behavioral Decision Theory."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIR = ARTICLE_ROOT / "python"

SCRIPTS = [
    "prospect_value_functions.py",
    "probability_weighting_models.py",
    "expected_utility_comparison.py",
    "framing_sensitivity_analysis.py",
    "loss_aversion_diagnostics.py",
    "behavioral_review_queue.py",
    "decision_record_exporter.py",
    "behavioral_decision_theory_simulation.py",
]


def main() -> None:
    for script in SCRIPTS:
        path = PYTHON_DIR / script
        print(f"Running {path.name}...")
        subprocess.run([sys.executable, str(path)], check=True)
    print("All Python behavioral decision workflows completed.")


if __name__ == "__main__":
    main()
