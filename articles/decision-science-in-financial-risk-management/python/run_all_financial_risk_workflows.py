#!/usr/bin/env python3
"""Run all Python workflows for Decision Science in Financial Risk Management."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIR = ARTICLE_ROOT / "python"

SCRIPTS = [
    "portfolio_loss_model.py",
    "capital_resilience_model.py",
    "liquidity_trigger_model.py",
    "model_risk_review.py",
    "financial_risk_strategy_comparison.py",
    "decision_record_exporter.py",
    "decision_science_financial_risk_simulation.py",
]


def main() -> None:
    for script in SCRIPTS:
        path = PYTHON_DIR / script
        print(f"Running {path.name}...")
        subprocess.run([sys.executable, str(path)], check=True)
    print("All Python financial-risk workflows completed.")


if __name__ == "__main__":
    main()
