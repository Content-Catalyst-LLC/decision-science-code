#!/usr/bin/env python3
"""Run all Python workflows for Decision Science and Systems Modeling."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIR = ARTICLE_ROOT / "python"

SCRIPTS = [
    "stock_flow_model.py",
    "feedback_loop_model.py",
    "delay_response_model.py",
    "threshold_risk_analysis.py",
    "scenario_strategy_comparison.py",
    "decision_record_exporter.py",
    "decision_science_systems_modeling_simulation.py",
]


def main() -> None:
    for script in SCRIPTS:
        path = PYTHON_DIR / script
        print(f"Running {path.name}...")
        subprocess.run([sys.executable, str(path)], check=True)
    print("All Python systems-modeling workflows completed.")


if __name__ == "__main__":
    main()
