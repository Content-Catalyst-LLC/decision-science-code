#!/usr/bin/env python3
"""Run all Python workflows for Path Dependence, Lock-In, and Decision Timing."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIR = ARTICLE_ROOT / "python"

SCRIPTS = [
    "switching_cost_model.py",
    "lock_in_risk_model.py",
    "option_value_decay_model.py",
    "timing_review_model.py",
    "path_strategy_comparison.py",
    "decision_record_exporter.py",
    "path_dependence_lock_in_decision_timing_simulation.py",
]


def main() -> None:
    for script in SCRIPTS:
        path = PYTHON_DIR / script
        print(f"Running {path.name}...")
        subprocess.run([sys.executable, str(path)], check=True)
    print("All Python path-dependence workflows completed.")


if __name__ == "__main__":
    main()
