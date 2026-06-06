#!/usr/bin/env python3
"""
Decision Science in Healthcare workflow.

Simulates hospital capacity, arrivals, discharges, queue pressure,
safety risk, surge response, and decision-record export.

Uses only the Python standard library.
"""

from __future__ import annotations

from pathlib import Path
import csv
import json
import random
from statistics import mean

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
DATA = ARTICLE_ROOT / "data"
TABLES = ARTICLE_ROOT / "outputs" / "tables"
RECORDS = ARTICLE_ROOT / "outputs" / "decision_records"


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def load_parameters() -> dict[str, float]:
    return {
        row["parameter"]: float(row["value"])
        for row in read_csv_dicts(DATA / "synthetic_system_parameters.csv")
    }


def simulate_hospital_system() -> list[dict[str, object]]:
    parameters = load_parameters()
    random.seed(int(parameters["random_seed"]))

    time_steps = int(parameters["time_steps"])
    queue = parameters["initial_queue"]
    staffing_capacity = parameters["initial_staffing_capacity"]
    discharge_capacity = parameters["initial_discharge_capacity"]
    surge_response = parameters["initial_surge_response"]
    safety_risk = parameters["initial_safety_risk"]
    queue_trigger = parameters["queue_trigger"]
    safety_risk_trigger = parameters["safety_risk_trigger"]

    rows: list[dict[str, object]] = []

    for time in range(1, time_steps + 1):
        arrivals = max(0.0, random.gauss(24.0, 4.5))
        staffing_variation = random.gauss(0.0, 1.8)
        effective_staffing = max(5.0, staffing_capacity + staffing_variation + 0.35 * surge_response)

        discharges = max(
            0.0,
            random.gauss(discharge_capacity, 3.2)
            + 0.20 * effective_staffing
            - 0.05 * queue
        )

        queue = max(0.0, queue + arrivals - discharges)

        queue_pressure = min(1.0, queue / 60.0)
        staffing_pressure = max(0.0, 1.0 - effective_staffing / 35.0)

        safety_risk = min(
            1.0,
            max(
                0.0,
                0.18 + 0.55 * queue_pressure + 0.28 * staffing_pressure + random.gauss(0.0, 0.03)
            )
        )

        surge_triggered = queue >= queue_trigger or safety_risk >= safety_risk_trigger

        if surge_triggered:
            surge_response = min(20.0, surge_response + 2.0)
            staffing_capacity = min(34.0, staffing_capacity + 0.35)
            discharge_capacity = min(30.0, discharge_capacity + 0.25)
        else:
            surge_response = max(0.0, surge_response - 0.50)

        service_continuity = max(
            0.0,
            min(
                1.0,
                0.92 - 0.45 * queue_pressure - 0.35 * safety_risk + 0.01 * surge_response
            )
        )

        rows.append({
            "time": time,
            "arrivals": round(arrivals, 6),
            "discharges": round(discharges, 6),
            "queue": round(queue, 6),
            "staffing_capacity": round(staffing_capacity, 6),
            "discharge_capacity": round(discharge_capacity, 6),
            "surge_response": round(surge_response, 6),
            "safety_risk": round(safety_risk, 6),
            "surge_triggered": surge_triggered,
            "service_continuity": round(service_continuity, 6),
        })

    return rows


def summarize(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    queue_values = [float(row["queue"]) for row in rows]
    safety_values = [float(row["safety_risk"]) for row in rows]
    continuity_values = [float(row["service_continuity"]) for row in rows]
    arrival_values = [float(row["arrivals"]) for row in rows]
    discharge_values = [float(row["discharges"]) for row in rows]
    surge_count = sum(1 for row in rows if bool(row["surge_triggered"]))

    return [
        {"metric": "average_queue", "value": round(mean(queue_values), 6)},
        {"metric": "maximum_queue", "value": round(max(queue_values), 6)},
        {"metric": "average_arrivals", "value": round(mean(arrival_values), 6)},
        {"metric": "average_discharges", "value": round(mean(discharge_values), 6)},
        {"metric": "average_safety_risk", "value": round(mean(safety_values), 6)},
        {"metric": "maximum_safety_risk", "value": round(max(safety_values), 6)},
        {"metric": "average_service_continuity", "value": round(mean(continuity_values), 6)},
        {"metric": "minimum_service_continuity", "value": round(min(continuity_values), 6)},
        {"metric": "surge_trigger_count", "value": surge_count},
    ]


def interpret(summary_rows: list[dict[str, object]], safety_trigger: float, queue_trigger: float) -> str:
    metrics = {str(row["metric"]): float(row["value"]) for row in summary_rows}

    if metrics["maximum_safety_risk"] >= safety_trigger:
        return "review_capacity_due_to_high_patient_safety_risk"
    if metrics["maximum_queue"] >= queue_trigger:
        return "activate_queue_reduction_and_surge_capacity_plan"
    if metrics["minimum_service_continuity"] < 0.45:
        return "redesign_patient_flow_and_discharge_capacity"
    return "continue_monitoring_with_adaptive_capacity_review"


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"No rows to write: {path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> None:
    parameters = load_parameters()
    rows = simulate_hospital_system()
    summary_rows = summarize(rows)
    recommendation = interpret(
        summary_rows,
        safety_trigger=parameters["safety_risk_trigger"],
        queue_trigger=parameters["queue_trigger"],
    )

    write_csv(TABLES / "healthcare_capacity_timeseries.csv", rows)
    write_csv(TABLES / "healthcare_capacity_summary.csv", summary_rows)

    write_json(
        RECORDS / "healthcare_decision_record.json",
        {
            "article": "Decision Science in Healthcare",
            "decision_context": "Simulating hospital capacity, queue pressure, patient safety risk, and adaptive surge response.",
            "parameters": parameters,
            "summary_metrics": summary_rows,
            "recommendation": recommendation,
            "modeling_principles": [
                "Healthcare decisions are probabilistic, operational, ethical, and patient-centered.",
                "Queue pressure can accumulate when arrivals exceed throughput over time.",
                "Safety risk rises when capacity, staffing, and flow are strained.",
                "Surge triggers should be connected to operational authority.",
                "Decision records should preserve assumptions, thresholds, patient-safety concerns, equity issues, and revision triggers."
            ],
        },
    )

    print("Decision science in healthcare simulation complete.")
    print(TABLES / "healthcare_capacity_timeseries.csv")
    print(TABLES / "healthcare_capacity_summary.csv")
    print(RECORDS / "healthcare_decision_record.json")


if __name__ == "__main__":
    main()
