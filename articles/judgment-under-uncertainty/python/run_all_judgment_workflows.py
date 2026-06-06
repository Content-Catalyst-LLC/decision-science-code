#!/usr/bin/env python3
"""Run all Python workflows for Judgment Under Uncertainty."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIR = ARTICLE_ROOT / "python"

SCRIPTS = [
    "bayesian_update_diagnostics.py",
    "calibration_error_scoring.py",
    "confidence_gap_analysis.py",
    "anchoring_distortion_model.py",
    "evidence_quality_profiles.py",
    "judgment_review_queue.py",
    "decision_record_exporter.py",
    "judgment_under_uncertainty_simulation.py",
]


def main() -> None:
    for script in SCRIPTS:
        path = PYTHON_DIR / script
        print(f"Running {path.name}...")
        subprocess.run([sys.executable, str(path)], check=True)
    print("All Python judgment workflows completed.")


if __name__ == "__main__":
    main()
