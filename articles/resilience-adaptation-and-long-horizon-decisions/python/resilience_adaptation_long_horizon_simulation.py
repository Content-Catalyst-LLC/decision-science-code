#!/usr/bin/env python3
"""
Resilience, Adaptation, and Long-Horizon Decisions workflow.

Simulates long-horizon system performance under repeated shocks,
adaptive recovery, resilience-capacity change, threshold review,
and decision-record export.

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


def simulate_resilience_pathway() -> list[dict[str, object]]:
    parameters = load_parameters()
    random.seed(int(parameters["random_seed"]))

    time_steps = int(parameters["time_steps"])
    system_state = parameters["initial_system_state"]
    resilience_capacity = parameters["initial_resilience_capacity"]
    threshold_failure_level = parameters["threshold_failure_level"]

    rows: list[dict[str, object]] = []

    for time in range(1, time_steps + 1):
        shock_load = max(0.0, random.gauss(8.0, 3.2))
        recovery = max(0.0, random.gauss(4.0 + resilience_capacity * 0.08, 1.4))
        adaptive_gain = max(0.0, random.gauss(1.2, 0.5))

        next_system_state = max(
            0.0,
            system_state - shock_load + recovery + adaptive_gain
        )

        next_resilience_capacity = max(
            0.0,
            resilience_capacity + adaptive_gain - shock_load * 0.06
        )

        threshold_breach = next_system_state <= threshold_failure_level

        rows.append({
            "time": time,
            "system_state": round(next_system_state, 6),
            "resilience_capacity": round(next_resilience_capacity, 6),
            "shock_load": round(shock_load, 6),
            "recovery": round(recovery, 6),
            "adaptive_gain": round(adaptive_gain, 6),
            "threshold_breach": threshold_breach,
        })

        system_state = next_system_state
        resilience_capacity = next_resilience_capacity

    return rows


def summarize(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    system_values = [float(row["system_state"]) for row in rows]
    resilience_values = [float(row["resilience_capacity"]) for row in rows]
    shock_values = [float(row["shock_load"]) for row in rows]
    recovery_values = [float(row["recovery"]) for row in rows]
    threshold_breaches = [row for row in rows if bool(row["threshold_breach"])]

    return [
        {"metric": "final_system_state", "value": round(system_values[-1], 6)},
        {"metric": "minimum_system_state", "value": round(min(system_values), 6)},
        {"metric": "average_system_state", "value": round(mean(system_values), 6)},
        {"metric": "final_resilience_capacity", "value": round(resilience_values[-1], 6)},
        {"metric": "average_resilience_capacity", "value": round(mean(resilience_values), 6)},
        {"metric": "average_shock_load", "value": round(mean(shock_values), 6)},
        {"metric": "average_recovery", "value": round(mean(recovery_values), 6)},
        {"metric": "threshold_breach_count", "value": len(threshold_breaches)},
        {"metric": "threshold_breach_rate", "value": round(len(threshold_breaches) / len(rows), 6)},
    ]


def interpret(summary_rows: list[dict[str, object]]) -> str:
    metrics = {str(row["metric"]): float(row["value"]) for row in summary_rows}
    threshold_failure_level = load_parameters()["threshold_failure_level"]

    if metrics["threshold_breach_rate"] > 0.20:
        return "redesign_strategy_due_to_repeated_resilience_threshold_breaches"
    if metrics["final_resilience_capacity"] < metrics["average_resilience_capacity"] * 0.75:
        return "increase_resilience_investment_and_monitor_capacity_depletion"
    if metrics["minimum_system_state"] < threshold_failure_level:
        return "define_adaptive_trigger_for_shock_response"
    return "continue_with_long_horizon_monitoring_and_adaptive_review"


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
    rows = simulate_resilience_pathway()
    summary_rows = summarize(rows)
    recommendation = interpret(summary_rows)
    parameters = load_parameters()

    write_csv(TABLES / "resilience_adaptive_recovery_timeseries.csv", rows)
    write_csv(TABLES / "resilience_adaptive_recovery_summary.csv", summary_rows)

    write_json(
        RECORDS / "resilience_adaptation_decision_record.json",
        {
            "article": "Resilience, Adaptation, and Long-Horizon Decisions",
            "decision_context": "Simulating long-horizon system performance under repeated shock, recovery, and adaptive capacity change.",
            "parameters": parameters,
            "summary_metrics": summary_rows,
            "recommendation": recommendation,
            "modeling_principles": [
                "Resilience capacity should be treated as a stock that can be built or depleted.",
                "Long-horizon strategies should be evaluated under repeated shocks rather than one stable forecast.",
                "Adaptive gains and recovery capacity shape long-run viability.",
                "Threshold breaches should trigger structured review.",
                "Decision records should preserve assumptions, indicators, thresholds, and revision triggers."
            ],
        },
    )

    print("Resilience, adaptation, and long-horizon simulation complete.")
    print(TABLES / "resilience_adaptive_recovery_timeseries.csv")
    print(TABLES / "resilience_adaptive_recovery_summary.csv")
    print(RECORDS / "resilience_adaptation_decision_record.json")


if __name__ == "__main__":
    main()
