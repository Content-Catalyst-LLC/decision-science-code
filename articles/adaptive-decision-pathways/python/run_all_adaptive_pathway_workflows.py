#!/usr/bin/env python3
"""Run all Python workflows for Adaptive Decision Pathways."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIR = ARTICLE_ROOT / "python"

SCRIPTS = [
    "pathway_score_model.py",
    "trigger_point_model.py",
    "option_value_model.py",
    "switching_rule_model.py",
    "pathway_comparison.py",
    "decision_record_exporter.py",
    "adaptive_decision_pathways_simulation.py",
]


def main() -> None:
    for script in SCRIPTS:
        path = PYTHON_DIR / script
        print(f"Running {path.name}...")
        subprocess.run([sys.executable, str(path)], check=True)
    print("All Python adaptive-pathway workflows completed.")


if __name__ == "__main__":
    main()
