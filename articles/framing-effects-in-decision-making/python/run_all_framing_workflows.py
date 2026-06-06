#!/usr/bin/env python3
"""Run all Python workflows for Framing Effects in Decision-Making."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIR = ARTICLE_ROOT / "python"

SCRIPTS = [
    "gain_loss_frame_model.py",
    "reference_point_sensitivity.py",
    "prospect_value_functions.py",
    "attribute_frame_diagnostics.py",
    "risk_communication_formats.py",
    "framing_review_queue.py",
    "decision_record_exporter.py",
    "framing_effects_decision_making_simulation.py",
]


def main() -> None:
    for script in SCRIPTS:
        path = PYTHON_DIR / script
        print(f"Running {path.name}...")
        subprocess.run([sys.executable, str(path)], check=True)
    print("All Python framing workflows completed.")


if __name__ == "__main__":
    main()
