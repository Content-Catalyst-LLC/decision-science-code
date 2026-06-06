#!/usr/bin/env python3
"""Run all Python workflows for Decision Hygiene and Bias Reduction."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIR = ARTICLE_ROOT / "python"

SCRIPTS = [
    "bias_noise_decomposition.py",
    "calibration_review.py",
    "evidence_quality_checks.py",
    "framing_bias_checks.py",
    "structured_dissent_review.py",
    "decision_hygiene_review_queue.py",
    "decision_record_exporter.py",
    "decision_hygiene_bias_reduction_simulation.py",
]


def main() -> None:
    for script in SCRIPTS:
        path = PYTHON_DIR / script
        print(f"Running {path.name}...")
        subprocess.run([sys.executable, str(path)], check=True)
    print("All Python decision hygiene workflows completed.")


if __name__ == "__main__":
    main()
