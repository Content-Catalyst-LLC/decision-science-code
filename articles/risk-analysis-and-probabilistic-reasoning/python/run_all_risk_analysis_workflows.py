#!/usr/bin/env python3
"""Run all Python workflows for Risk Analysis and Probabilistic Reasoning."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIR = ARTICLE_ROOT / "python"

SCRIPTS = [
    "expected_loss_calculator.py",
    "variance_and_tail_metrics.py",
    "value_at_risk_cvar.py",
    "threshold_breach_analysis.py",
    "scenario_stress_testing.py",
    "probability_quality_audit.py",
    "bayesian_risk_update.py",
    "decision_record_exporter.py",
    "risk_analysis_probabilistic_reasoning_simulation.py",
]


def main() -> None:
    for script in SCRIPTS:
        path = PYTHON_DIR / script
        print(f"Running {path.name}...")
        subprocess.run([sys.executable, str(path)], check=True)
    print("All Python risk-analysis workflows completed.")


if __name__ == "__main__":
    main()
