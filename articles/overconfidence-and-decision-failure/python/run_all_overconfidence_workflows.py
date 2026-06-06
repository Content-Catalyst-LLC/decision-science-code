#!/usr/bin/env python3
"""Run all Python workflows for Overconfidence and Decision Failure."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIR = ARTICLE_ROOT / "python"

SCRIPTS = [
    "confidence_error_diagnostics.py",
    "calibration_scoring.py",
    "interval_coverage_analysis.py",
    "planning_fallacy_model.py",
    "model_overconfidence_checks.py",
    "overconfidence_review_queue.py",
    "decision_record_exporter.py",
    "overconfidence_decision_failure_simulation.py",
]


def main() -> None:
    for script in SCRIPTS:
        path = PYTHON_DIR / script
        print(f"Running {path.name}...")
        subprocess.run([sys.executable, str(path)], check=True)
    print("All Python overconfidence workflows completed.")


if __name__ == "__main__":
    main()
