#!/usr/bin/env python3
"""Run all Python workflows for Regret Analysis and Minimax Decision Rules."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIR = ARTICLE_ROOT / "python"

SCRIPTS = [
    "payoff_matrix_builder.py",
    "regret_matrix_calculator.py",
    "maximin_rule.py",
    "minimax_regret_rule.py",
    "threshold_compliance.py",
    "vulnerability_analysis.py",
    "decision_rule_comparison.py",
    "decision_record_exporter.py",
    "regret_analysis_minimax_decision_rules_simulation.py",
]


def main() -> None:
    for script in SCRIPTS:
        path = PYTHON_DIR / script
        print(f"Running {path.name}...")
        subprocess.run([sys.executable, str(path)], check=True)
    print("All Python regret and minimax workflows completed.")


if __name__ == "__main__":
    main()
