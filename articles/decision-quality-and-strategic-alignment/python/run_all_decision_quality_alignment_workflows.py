#!/usr/bin/env python3
"""Run all Python workflows for Decision Quality and Strategic Alignment."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIR = ARTICLE_ROOT / "python"

SCRIPTS = [
    "decision_quality_score.py",
    "strategic_alignment_score.py",
    "implementation_readiness.py",
    "alignment_drift_analysis.py",
    "adaptive_performance_simulation.py",
    "decision_review_queue.py",
    "decision_record_exporter.py",
    "decision_quality_strategic_alignment_simulation.py",
]


def main() -> None:
    for script in SCRIPTS:
        path = PYTHON_DIR / script
        print(f"Running {path.name}...")
        subprocess.run([sys.executable, str(path)], check=True)
    print("All Python decision quality and alignment workflows completed.")


if __name__ == "__main__":
    main()
