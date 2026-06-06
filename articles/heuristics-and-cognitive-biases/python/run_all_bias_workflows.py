#!/usr/bin/env python3
"""Run all Python workflows for Heuristics and Cognitive Biases."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIR = ARTICLE_ROOT / "python"

SCRIPTS = [
    "anchoring_bias_model.py",
    "availability_bias_model.py",
    "representativeness_bias_model.py",
    "confirmation_bias_diagnostics.py",
    "confidence_distortion_analysis.py",
    "calibration_error_scoring.py",
    "debiasing_review_queue.py",
    "decision_record_exporter.py",
    "heuristics_cognitive_biases_simulation.py",
]


def main() -> None:
    for script in SCRIPTS:
        path = PYTHON_DIR / script
        print(f"Running {path.name}...")
        subprocess.run([sys.executable, str(path)], check=True)
    print("All Python bias workflows completed.")


if __name__ == "__main__":
    main()
