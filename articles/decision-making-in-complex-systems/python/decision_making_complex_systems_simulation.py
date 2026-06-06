#!/usr/bin/env python3
"""
Decision-Making in Complex Systems workflow.

Simulates adaptive choice under interdependence, spillover pressure,
feedback, shocks, threshold risk, and institutional capacity.

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

RANDOM_SEED = 42


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def load_parameters() -> dict[str, float]:
    return {
        row["parameter"]: float(row["value"])
        for row in read_csv_dicts(DATA / "synthetic_system_parameters.csv")
    }


def simulate_system() -> list[dict[str, object]]:
    parameters = load_parameters()
    random.seed(RANDOM_SEED)

    time_steps = int(parameters["time_steps"])
    target_state = parameters["target_state"]
    threshold_risk_level = parameters["threshold_risk_level"]

    system_state = parameters["initial_system_state"]
    adaptive_response = parameters["initial_adaptive_response"]
    spillover_pressure = parameters["initial_spillover_pressure"]
    institutional_capacity = parameters["initial_institutional_capacity"]

    rows: list[dict[str, object]] = []

    for time in range(1, time_steps + 1):
        shock = random.gauss(0, 2.4)
        spillover_effect = 0.08 * spillover_pressure
        adaptation_effect = 0.10 * adaptive_response
        capacity_effect = 0.04 * (institutional_capacity - 50.0)

        next_system_state = max(
            0.0,
            system_state + shock + spillover_effect - adaptation_effect - capacity_effect
        )

        next_adaptive_response = max(
            0.0,
            adaptive_response + 0.06 * (target_state - system_state)
        )

        next_spillover_pressure = max(
            0.0,
            spillover_pressure + 0.05 * system_state - 0.03 * adaptive_response
        )

        next_institutional_capacity = max(
            0.0,
            institutional_capacity + 0.03 * adaptive_response - 0.02 * spillover_pressure
        )

        threshold_breach = next_system_state >= threshold_risk_level

        rows.append({
            "time": time,
            "system_state": round(next_system_state, 6),
            "adaptive_response": round(next_adaptive_response, 6),
            "spillover_pressure": round(next_spillover_pressure, 6),
            "institutional_capacity": round(next_institutional_capacity, 6),
            "shock": round(shock, 6),
            "threshold_breach": threshold_breach,
        })

        system_state = next_system_state
        adaptive_response = next_adaptive_response
        spillover_pressure = next_spillover_pressure
        institutional_capacity = next_institutional_capacity

    return rows


def summarize(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    system_values = [float(row["system_state"]) for row in rows]
    adaptive_values = [float(row["adaptive_response"]) for row in rows]
    spillover_values = [float(row["spillover_pressure"]) for row in rows]
    capacity_values = [float(row["institutional_capacity"]) for row in rows]
    threshold_breaches = [row for row in rows if bool(row["threshold_breach"])]

    return [
        {"metric": "final_system_state", "value": round(system_values[-1], 6)},
        {"metric": "average_system_state", "value": round(mean(system_values), 6)},
        {"metric": "minimum_system_state", "value": round(min(system_values), 6)},
        {"metric": "maximum_system_state", "value": round(max(system_values), 6)},
        {"metric": "average_adaptive_response", "value": round(mean(adaptive_values), 6)},
        {"metric": "average_spillover_pressure", "value": round(mean(spillover_values), 6)},
        {"metric": "average_institutional_capacity", "value": round(mean(capacity_values), 6)},
        {"metric": "threshold_breach_count", "value": len(threshold_breaches)},
        {"metric": "threshold_breach_rate", "value": round(len(threshold_breaches) / len(rows), 6)},
    ]


def decision_interpretation(summary_rows: list[dict[str, object]]) -> str:
    metrics = {str(row["metric"]): float(row["value"]) for row in summary_rows}

    if metrics["threshold_breach_rate"] > 0.20:
        return "review_strategy_due_to_threshold_breach"
    if metrics["average_spillover_pressure"] > metrics["average_adaptive_response"]:
        return "increase_adaptive_capacity_and_spillover_monitoring"
    if metrics["final_system_state"] < 58.0:
        return "maintain_adaptive_response_and_monitor_feedback"
    return "continue_with_structured_review"


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
    rows = simulate_system()
    summary_rows = summarize(rows)
    recommendation = decision_interpretation(summary_rows)
    parameters = load_parameters()

    write_csv(TABLES / "complex_system_simulation_timeseries.csv", rows)
    write_csv(TABLES / "complex_system_simulation_summary.csv", summary_rows)

    write_json(
        RECORDS / "complex_system_decision_record.json",
        {
            "article": "Decision-Making in Complex Systems",
            "decision_context": "Simulating adaptive choice under interdependence, spillover pressure, shocks, and threshold risk.",
            "random_seed": RANDOM_SEED,
            "parameters": parameters,
            "summary_metrics": summary_rows,
            "recommendation": recommendation,
            "modeling_principles": [
                "Complex-system decisions change the system state they later observe.",
                "Feedback, delay, spillover, and adaptation should be monitored after action.",
                "Threshold breaches should trigger review rather than retrospective blame alone.",
                "Adaptive response should be evaluated against spillover pressure and institutional capacity.",
                "Decision records should preserve assumptions, indicators, and review triggers."
            ],
        },
    )

    print("Decision-making in complex systems simulation complete.")
    print(TABLES / "complex_system_simulation_timeseries.csv")
    print(TABLES / "complex_system_simulation_summary.csv")
    print(RECORDS / "complex_system_decision_record.json")


if __name__ == "__main__":
    main()
