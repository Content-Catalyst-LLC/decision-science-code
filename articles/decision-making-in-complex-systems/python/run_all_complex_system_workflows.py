#!/usr/bin/env python3
"""Run all Python workflows for Decision-Making in Complex Systems."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIR = ARTICLE_ROOT / "python"

SCRIPTS = [
    "feedback_loop_model.py",
    "adaptive_response_model.py",
    "spillover_pressure_model.py",
    "threshold_risk_analysis.py",
    "strategy_comparison.py",
    "decision_record_exporter.py",
    "decision_making_complex_systems_simulation.py",
]


def main() -> None:
    for script in SCRIPTS:
        path = PYTHON_DIR / script
        print(f"Running {path.name}...")
        subprocess.run([sys.executable, str(path)], check=True)
    print("All Python complex-system workflows completed.")


if __name__ == "__main__":
    main()
