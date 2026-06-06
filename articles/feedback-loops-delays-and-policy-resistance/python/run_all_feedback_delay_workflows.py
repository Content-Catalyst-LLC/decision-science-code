#!/usr/bin/env python3
"""Run all Python workflows for Feedback Loops, Delays, and Policy Resistance."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIR = ARTICLE_ROOT / "python"

SCRIPTS = [
    "reinforcing_feedback_model.py",
    "balancing_feedback_model.py",
    "delay_response_model.py",
    "policy_resistance_model.py",
    "threshold_review.py",
    "scenario_policy_comparison.py",
    "decision_record_exporter.py",
    "feedback_loops_delays_policy_resistance_simulation.py",
]


def main() -> None:
    for script in SCRIPTS:
        path = PYTHON_DIR / script
        print(f"Running {path.name}...")
        subprocess.run([sys.executable, str(path)], check=True)
    print("All Python feedback-delay workflows completed.")


if __name__ == "__main__":
    main()
