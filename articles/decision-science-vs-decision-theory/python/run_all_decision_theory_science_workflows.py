#!/usr/bin/env python3
"""Run all Python workflows for Decision Science vs. Decision Theory."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIR = ARTICLE_ROOT / "python"

SCRIPTS = [
    "expected_utility_comparison.py",
    "bayesian_update_decision_rule.py",
    "minimax_regret_diagnostics.py",
    "satisficing_agent_model.py",
    "robust_adaptive_strategy_scan.py",
    "institutional_stress_testing.py",
    "decision_record_exporter.py",
    "decision_science_vs_decision_theory_simulation.py",
]


def main() -> None:
    for script in SCRIPTS:
        path = PYTHON_DIR / script
        print(f"Running {path.name}...")
        subprocess.run([sys.executable, str(path)], check=True)
    print("All Python decision theory/science workflows completed.")


if __name__ == "__main__":
    main()
