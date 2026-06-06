#!/usr/bin/env python3
"""
Decision Science and Systems Modeling workflow.

Simulates dynamic system response to repeated decisions, delayed correction,
resilience capacity, threshold risk, and decision-record export.

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
    delay = int(parameters["delay"])

    system_state = parameters["initial_system_state"]
    intervention_signal = parameters["initial_intervention_signal"]
    resilience_capacity = parameters["initial_resilience_capacity"]

    intervention_history = [intervention_signal]
    rows: list[dict[str, object]] = []

    for time in range(1, time_steps + 1):
        delayed_index = max(0, len(intervention_history) - delay)
        delayed_intervention = intervention_history[delayed_index]

        pressure = 0.07 * system_state
        correction = 0.12 * delayed_intervention
        resilience_gain = 0.05 * resilience_capacity
        disturbance = random.gauss(0.0, 1.0)

        next_system_state = max(
            0.0,
            system_state + pressure - correction - resilience_gain + disturbance
        )

        next_intervention_signal = max(
            0.0,
            intervention_signal + 0.05 * (target_state - system_state)
        )

        next_resilience_capacity = max(
            0.0,
            resilience_capacity + 0.04 * intervention_signal - 0.02 * system_state
        )

        threshold_breach = next_system_state >= threshold_risk_level

        rows.append({
            "time": time,
            "system_state": round(next_system_state, 6),
            "intervention_signal": round(next_intervention_signal, 6),
            "resilience_capacity": round(next_resilience_capacity, 6),
            "delayed_intervention": round(delayed_intervention, 6),
            "pressure": round(pressure, 6),
            "correction": round(correction, 6),
            "resilience_gain": round(resilience_gain, 6),
            "disturbance": round(disturbance, 6),
            "threshold_breach": threshold_breach,
        })

        system_state = next_system_state
        intervention_signal = next_intervention_signal
        resilience_capacity = next_resilience_capacity
        intervention_history.append(intervention_signal)

    return rows


def summarize(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    system_values = [float(row["system_state"]) for row in rows]
    intervention_values = [float(row["intervention_signal"]) for row in rows]
    resilience_values = [float(row["resilience_capacity"]) for row in rows]
    threshold_breaches = [row for row in rows if bool(row["threshold_breach"])]

    return [
        {"metric": "final_system_state", "value": round(system_values[-1], 6)},
        {"metric": "peak_system_state", "value": round(max(system_values), 6)},
        {"metric": "average_system_state", "value": round(mean(system_values), 6)},
        {"metric": "average_intervention_signal", "value": round(mean(intervention_values), 6)},
        {"metric": "average_resilience_capacity", "value": round(mean(resilience_values), 6)},
        {"metric": "threshold_breach_count", "value": len(threshold_breaches)},
        {"metric": "threshold_breach_rate", "value": round(len(threshold_breaches) / len(rows), 6)},
    ]


def interpret(summary_rows: list[dict[str, object]]) -> str:
    metrics = {str(row["metric"]): float(row["value"]) for row in summary_rows}
    parameters = load_parameters()
    threshold_risk_level = parameters["threshold_risk_level"]

    if metrics["threshold_breach_rate"] > 0.20:
        return "review_policy_due_to_threshold_breach"
    if metrics["peak_system_state"] > threshold_risk_level:
        return "strengthen_early_warning_and_delay_controls"
    if metrics["average_resilience_capacity"] < 10.0:
        return "increase_resilience_capacity"
    return "continue_with_monitoring_and_structured_review"


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
    recommendation = interpret(summary_rows)
    parameters = load_parameters()

    write_csv(TABLES / "systems_modeling_simulation_timeseries.csv", rows)
    write_csv(TABLES / "systems_modeling_simulation_summary.csv", summary_rows)

    write_json(
        RECORDS / "systems_modeling_decision_record.json",
        {
            "article": "Decision Science and Systems Modeling",
            "decision_context": "Simulating dynamic system response to repeated decisions, delayed correction, resilience capacity, and threshold risk.",
            "random_seed": RANDOM_SEED,
            "parameters": parameters,
            "summary_metrics": summary_rows,
            "recommendation": recommendation,
            "modeling_principles": [
                "Decisions should be represented as interventions in dynamic systems.",
                "Delayed effects can distort early interpretation of outcomes.",
                "Stocks, flows, feedback, and resilience capacity shape system response.",
                "Threshold breaches should trigger review and model revision.",
                "Decision records should preserve assumptions, model structure, and monitoring triggers."
            ],
        },
    )

    print("Decision science and systems modeling simulation complete.")
    print(TABLES / "systems_modeling_simulation_timeseries.csv")
    print(TABLES / "systems_modeling_simulation_summary.csv")
    print(RECORDS / "systems_modeling_decision_record.json")


if __name__ == "__main__":
    main()
