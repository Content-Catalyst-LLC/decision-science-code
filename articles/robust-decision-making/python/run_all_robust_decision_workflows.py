#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import subprocess
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIR = ARTICLE_ROOT / "python"
SCRIPTS = [
    "expected_value_model.py",
    "worst_case_analysis.py",
    "regret_analysis.py",
    "threshold_compliance.py",
    "vulnerability_analysis.py",
    "adaptive_trigger_review.py",
    "decision_record_exporter.py",
    "robust_decision_making_simulation.py",
]

def main() -> None:
    for script in SCRIPTS:
        path = PYTHON_DIR / script
        print(f"Running {path.name}...")
        subprocess.run([sys.executable, str(path)], check=True)
    print("All Python robust decision workflows completed.")

if __name__ == "__main__":
    main()
