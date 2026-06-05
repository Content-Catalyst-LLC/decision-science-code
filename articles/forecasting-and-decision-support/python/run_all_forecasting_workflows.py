#!/usr/bin/env python3
"""Run all Python workflows for Forecasting and Decision Support."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIR = ARTICLE_ROOT / "python"

SCRIPTS = [
    "forecast_error_metrics.py",
    "probabilistic_forecast_calibration.py",
    "decision_threshold_forecasts.py",
    "forecast_value_of_information.py",
    "horizon_degradation_analysis.py",
    "reference_class_forecasting.py",
    "early_warning_signal_monitoring.py",
    "decision_record_exporter.py",
    "forecasting_decision_support_simulation.py",
]


def main() -> None:
    for script in SCRIPTS:
        path = PYTHON_DIR / script
        print(f"Running {path.name}...")
        subprocess.run([sys.executable, str(path)], check=True)
    print("All Python forecasting workflows completed.")


if __name__ == "__main__":
    main()
