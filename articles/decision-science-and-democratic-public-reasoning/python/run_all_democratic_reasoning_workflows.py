#!/usr/bin/env python3
"""Run all Python workflows for Decision Science and Democratic Public Reasoning."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIR = ARTICLE_ROOT / "python"

SCRIPTS = [
    "legitimacy_model.py",
    "contestability_model.py",
    "public_trust_model.py",
    "democratic_process_comparison.py",
    "decision_record_exporter.py",
    "democratic_public_reasoning_simulation.py",
]


def main() -> None:
    for script in SCRIPTS:
        path = PYTHON_DIR / script
        print(f"Running {path.name}...")
        subprocess.run([sys.executable, str(path)], check=True)
    print("All Python democratic-public-reasoning workflows completed.")


if __name__ == "__main__":
    main()
