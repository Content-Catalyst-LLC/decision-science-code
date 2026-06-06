#!/usr/bin/env python3
"""Run all Python workflows for Cascading Risk and Systemic Decision Failure."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIR = ARTICLE_ROOT / "python"

SCRIPTS = [
    "cascade_risk_score_model.py",
    "threshold_failure_model.py",
    "buffer_depletion_model.py",
    "common_mode_risk_model.py",
    "system_vulnerability_comparison.py",
    "decision_record_exporter.py",
    "cascading_risk_systemic_failure_simulation.py",
]


def main() -> None:
    for script in SCRIPTS:
        path = PYTHON_DIR / script
        print(f"Running {path.name}...")
        subprocess.run([sys.executable, str(path)], check=True)
    print("All Python cascading-risk workflows completed.")


if __name__ == "__main__":
    main()
