#!/usr/bin/env python3
"""Run all Python workflows for Decision Trees and Structured Choice."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIR = ARTICLE_ROOT / "python"

SCRIPTS = [
    "expected_value_rollback.py",
    "chance_node_evaluator.py",
    "decision_node_selector.py",
    "value_of_information_analysis.py",
    "probability_threshold_analysis.py",
    "regret_profile_analysis.py",
    "review_trigger_generator.py",
    "decision_record_exporter.py",
    "decision_trees_structured_choice_simulation.py",
]


def main() -> None:
    for script in SCRIPTS:
        path = PYTHON_DIR / script
        print(f"Running {path.name}...")
        subprocess.run([sys.executable, str(path)], check=True)
    print("All Python decision-tree workflows completed.")


if __name__ == "__main__":
    main()
