#!/usr/bin/env python3
"""Run all Python workflows for Decision Governance and Institutional Accountability."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIR = ARTICLE_ROOT / "python"

SCRIPTS = [
    "accountability_model.py",
    "responsibility_gap_model.py",
    "review_trigger_model.py",
    "governance_design_comparison.py",
    "decision_record_exporter.py",
    "decision_governance_accountability_simulation.py",
]


def main() -> None:
    for script in SCRIPTS:
        path = PYTHON_DIR / script
        print(f"Running {path.name}...")
        subprocess.run([sys.executable, str(path)], check=True)
    print("All Python decision-governance workflows completed.")


if __name__ == "__main__":
    main()
