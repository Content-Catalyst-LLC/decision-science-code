#!/usr/bin/env python3
"""Run all Python workflows for Future Directions in Decision Science."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIR = ARTICLE_ROOT / "python"

SCRIPTS = [
    "future_maturity_model.py",
    "ai_reliance_model.py",
    "adaptive_review_model.py",
    "future_pathway_comparison.py",
    "decision_record_exporter.py",
    "future_decision_science_simulation.py",
]


def main() -> None:
    for script in SCRIPTS:
        path = PYTHON_DIR / script
        print(f"Running {path.name}...")
        subprocess.run([sys.executable, str(path)], check=True)
    print("All Python future decision-science workflows completed.")


if __name__ == "__main__":
    main()
