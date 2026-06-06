#!/usr/bin/env python3
from pathlib import Path
import subprocess, sys

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = [
    "ethical_risk_model.py",
    "distributional_impact_model.py",
    "legitimacy_model.py",
    "ethical_decision_comparison.py",
    "decision_record_exporter.py",
    "ethics_of_decision_science_simulation.py",
]

for script in SCRIPTS:
    path = ROOT / "python" / script
    print(f"Running {path.name}...")
    subprocess.run([sys.executable, str(path)], check=True)

print("All Python ethics workflows completed.")
