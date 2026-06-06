#!/usr/bin/env python3
"""Run all Python workflows for Decision Science in Infrastructure Planning."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIR = ARTICLE_ROOT / "python"

SCRIPTS = [
    "infrastructure_alternative_model.py",
    "lifecycle_cost_model.py",
    "resilience_score_model.py",
    "adaptive_trigger_model.py",
    "infrastructure_strategy_comparison.py",
    "decision_record_exporter.py",
    "decision_science_infrastructure_planning_simulation.py",
]


def main() -> None:
    for script in SCRIPTS:
        path = PYTHON_DIR / script
        print(f"Running {path.name}...")
        subprocess.run([sys.executable, str(path)], check=True)
    print("All Python infrastructure workflows completed.")


if __name__ == "__main__":
    main()
