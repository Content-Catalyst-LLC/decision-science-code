#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIR = ARTICLE_ROOT / "python"

SCRIPTS = [
    "crisis_risk_model.py",
    "escalation_trigger_model.py",
    "trust_and_communication_model.py",
    "crisis_response_comparison.py",
    "decision_record_exporter.py",
    "decision_science_crisis_management_simulation.py",
]

def main() -> None:
    for script in SCRIPTS:
        print(f"Running {script}...")
        subprocess.run([sys.executable, str(PYTHON_DIR / script)], check=True)
    print("All Python crisis-management workflows completed.")

if __name__ == "__main__":
    main()
