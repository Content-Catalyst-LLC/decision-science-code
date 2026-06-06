#!/usr/bin/env python3
"""Run all Python workflows for Group Decision-Making and Social Influence."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIR = ARTICLE_ROOT / "python"

SCRIPTS = [
    "influence_weight_diagnostics.py",
    "hidden_profile_risk_analysis.py",
    "dissent_signal_summary.py",
    "consensus_pressure_model.py",
    "collective_error_scoring.py",
    "group_decision_review_queue.py",
    "decision_record_exporter.py",
    "group_decision_social_influence_simulation.py",
]


def main() -> None:
    for script in SCRIPTS:
        path = PYTHON_DIR / script
        print(f"Running {path.name}...")
        subprocess.run([sys.executable, str(path)], check=True)
    print("All Python group decision workflows completed.")


if __name__ == "__main__":
    main()
