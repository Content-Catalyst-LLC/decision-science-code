#!/usr/bin/env python3
"""Run all Python workflows for Decision Records and Accountable Judgment."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIR = ARTICLE_ROOT / "python"

SCRIPTS = [
    "decision_record_completeness_score.py",
    "evidence_traceability_checker.py",
    "assumption_criticality_audit.py",
    "dissent_preservation_audit.py",
    "review_trigger_monitor.py",
    "post_decision_learning_loop.py",
    "decision_record_exporter.py",
    "decision_records_accountable_judgment_audit.py",
]


def main() -> None:
    for script in SCRIPTS:
        path = PYTHON_DIR / script
        print(f"Running {path.name}...")
        subprocess.run([sys.executable, str(path)], check=True)
    print("All Python decision-record workflows completed.")


if __name__ == "__main__":
    main()
