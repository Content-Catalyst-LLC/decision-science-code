#!/usr/bin/env python3
"""Run all Python workflows for Core Principles of Decision Science."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIR = ARTICLE_ROOT / "python"

SCRIPTS = [
    "decision_framing_diagnostics.py",
    "uncertainty_representation_score.py",
    "tradeoff_weight_sensitivity.py",
    "behavioral_safeguard_audit.py",
    "systems_consequence_scan.py",
    "robustness_threshold_analysis.py",
    "decision_record_exporter.py",
    "adaptive_decision_quality_simulation.py",
]


def main() -> None:
    for script in SCRIPTS:
        path = PYTHON_DIR / script
        print(f"Running {path.name}...")
        subprocess.run([sys.executable, str(path)], check=True)
    print("All Python core principles workflows completed.")


if __name__ == "__main__":
    main()
