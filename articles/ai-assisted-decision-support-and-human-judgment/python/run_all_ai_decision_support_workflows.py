#!/usr/bin/env python3
"""Run all Python workflows for AI-Assisted Decision Support and Human Judgment."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIR = ARTICLE_ROOT / "python"

SCRIPTS = [
    "model_reliance_model.py",
    "automation_bias_model.py",
    "oversight_trigger_model.py",
    "ai_decision_support_comparison.py",
    "decision_record_exporter.py",
    "ai_assisted_decision_support_simulation.py",
]


def main() -> None:
    for script in SCRIPTS:
        path = PYTHON_DIR / script
        print(f"Running {path.name}...")
        subprocess.run([sys.executable, str(path)], check=True)
    print("All Python AI decision-support workflows completed.")


if __name__ == "__main__":
    main()
