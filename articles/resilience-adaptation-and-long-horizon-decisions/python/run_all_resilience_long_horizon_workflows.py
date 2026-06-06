#!/usr/bin/env python3
"""Run all Python workflows for Resilience, Adaptation, and Long-Horizon Decisions."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIR = ARTICLE_ROOT / "python"

SCRIPTS = [
    "resilience_stock_model.py",
    "adaptive_revision_model.py",
    "shock_absorption_model.py",
    "threshold_review_model.py",
    "long_horizon_strategy_comparison.py",
    "decision_record_exporter.py",
    "resilience_adaptation_long_horizon_simulation.py",
]


def main() -> None:
    for script in SCRIPTS:
        path = PYTHON_DIR / script
        print(f"Running {path.name}...")
        subprocess.run([sys.executable, str(path)], check=True)
    print("All Python resilience long-horizon workflows completed.")


if __name__ == "__main__":
    main()
