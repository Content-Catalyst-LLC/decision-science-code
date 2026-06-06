#!/usr/bin/env python3
"""Run all Python workflows for Bounded Rationality."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIR = ARTICLE_ROOT / "python"

SCRIPTS = [
    "satisficing_search_model.py",
    "optimizing_vs_satisficing.py",
    "aspiration_adaptation.py",
    "search_cost_diagnostics.py",
    "organizational_constraint_model.py",
    "stopping_rule_analysis.py",
    "decision_record_exporter.py",
    "bounded_rationality_simulation.py",
]


def main() -> None:
    for script in SCRIPTS:
        path = PYTHON_DIR / script
        print(f"Running {path.name}...")
        subprocess.run([sys.executable, str(path)], check=True)
    print("All Python bounded rationality workflows completed.")


if __name__ == "__main__":
    main()
