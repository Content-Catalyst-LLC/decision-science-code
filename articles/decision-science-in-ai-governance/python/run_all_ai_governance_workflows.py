#!/usr/bin/env python3
"""Run all Python workflows for Decision Science in AI Governance."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIR = ARTICLE_ROOT / "python"

SCRIPTS = [
    "ai_risk_model.py",
    "oversight_capacity_model.py",
    "drift_trigger_model.py",
    "ai_governance_strategy_comparison.py",
    "decision_record_exporter.py",
    "decision_science_ai_governance_simulation.py",
]


def main() -> None:
    for script in SCRIPTS:
        path = PYTHON_DIR / script
        print(f"Running {path.name}...")
        subprocess.run([sys.executable, str(path)], check=True)
    print("All Python AI-governance workflows completed.")


if __name__ == "__main__":
    main()
