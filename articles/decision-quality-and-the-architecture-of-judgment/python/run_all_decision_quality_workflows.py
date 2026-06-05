#!/usr/bin/env python3
"""Run all Python workflows for Decision Quality and the Architecture of Judgment."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIR = ARTICLE_ROOT / "python"

SCRIPTS = [
    "process_vs_outcome_quality.py",
    "decision_quality_scorecard.py",
    "outcome_bias_diagnostics.py",
    "judgment_architecture_audit.py",
    "luck_vs_skill_simulation.py",
    "review_trigger_generator.py",
    "decision_record_exporter.py",
    "decision_quality_architecture_simulation.py",
]


def main() -> None:
    for script in SCRIPTS:
        path = PYTHON_DIR / script
        print(f"Running {path.name}...")
        subprocess.run([sys.executable, str(path)], check=True)
    print("All Python decision-quality workflows completed.")


if __name__ == "__main__":
    main()
