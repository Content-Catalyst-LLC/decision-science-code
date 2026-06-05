#!/usr/bin/env python3
"""Run all Python workflows for Probability Calibration and Decision Confidence."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIR = ARTICLE_ROOT / "python"

SCRIPTS = [
    "brier_score_calculator.py",
    "log_loss_calculator.py",
    "reliability_table_builder.py",
    "expected_calibration_error.py",
    "confidence_bias_diagnostics.py",
    "decision_threshold_calibration.py",
    "base_rate_reference_class_checks.py",
    "decision_record_exporter.py",
    "probability_calibration_decision_confidence_simulation.py",
]


def main() -> None:
    for script in SCRIPTS:
        path = PYTHON_DIR / script
        print(f"Running {path.name}...")
        subprocess.run([sys.executable, str(path)], check=True)
    print("All Python calibration workflows completed.")


if __name__ == "__main__":
    main()
