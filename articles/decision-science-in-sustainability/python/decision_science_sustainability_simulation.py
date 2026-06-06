#!/usr/bin/env python3
"""
Decision Science in Sustainability workflow.

Simulates resource pressure, regeneration, adaptive policy response,
threshold risk, governance delay, public trust, and decision-record export.

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


def simulate_sustainability_system() -> list[dict[str, object]]:
    parameters = load_parameters()
    random.seed(int(parameters["random_seed"]))

    time_steps = int(parameters["time_steps"])
    resource_stock = parameters["initial_resource_stock"]
    resource_pressure = parameters["initial_resource_pressure"]
    policy_response = parameters["initial_policy_response"]
    public_trust = parameters["initial_public_trust"]
    implementation_capacity = parameters["initial_implementation_capacity"]
    governance_delay = parameters["initial_governance_delay"]
    resource_threshold = parameters["resource_threshold"]

    rows: list[dict[str, object]] = []

    for time in range(1, time_steps + 1):
        extraction = max(0.0, random.gauss(resource_pressure, 2.5))
        regeneration = max(0.0, random.gauss(10.0 + 0.40 * policy_response, 1.8))

        resource_stock = max(0.0, resource_stock - extraction + regeneration)

        threshold_gap = max(0.0, resource_threshold - resource_stock)

        pressure_change = (
            random.gauss(0.60, 0.70)
            - 0.050 * policy_response
            + 0.030 * governance_delay
        )

        policy_change = (
            0.080 * threshold_gap
            + 0.020 * public_trust
            + 0.030 * implementation_capacity
            - 0.050 * governance_delay
            + random.gauss(0.0, 0.30)
        )

        capacity_change = (
            0.020 * policy_response
            - 0.030 * governance_delay
            + random.gauss(0.20, 0.20)
        )

        trust_change = (
            0.020 * resource_stock
            - 0.030 * resource_pressure
            - 0.020 * governance_delay
            + random.gauss(0.0, 0.40)
        ) / 10.0

        resource_pressure = max(5.0, resource_pressure + pressure_change)
        policy_response = max(0.0, policy_response + policy_change)
        implementation_capacity = max(0.0, implementation_capacity + capacity_change)
        public_trust = max(0.0, min(100.0, public_trust + trust_change))
        governance_delay = max(0.0, governance_delay + random.gauss(0.05, 0.20) - 0.010 * implementation_capacity)

        threshold_breach = resource_stock < resource_threshold

        sustainability_score = (
            0.36 * resource_stock
            + 0.20 * policy_response
            + 0.18 * public_trust
            + 0.16 * implementation_capacity
            - 0.20 * resource_pressure
            - 0.10 * governance_delay
        )

        rows.append({
            "time": time,
            "resource_stock": round(resource_stock, 6),
            "resource_pressure": round(resource_pressure, 6),
            "policy_response": round(policy_response, 6),
            "public_trust": round(public_trust, 6),
            "implementation_capacity": round(implementation_capacity, 6),
            "governance_delay": round(governance_delay, 6),
            "threshold_breach": threshold_breach,
            "sustainability_score": round(sustainability_score, 6),
        })

    return rows


def summarize(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    resource_values = [float(row["resource_stock"]) for row in rows]
    pressure_values = [float(row["resource_pressure"]) for row in rows]
    response_values = [float(row["policy_response"]) for row in rows]
    trust_values = [float(row["public_trust"]) for row in rows]
    capacity_values = [float(row["implementation_capacity"]) for row in rows]
    delay_values = [float(row["governance_delay"]) for row in rows]
    score_values = [float(row["sustainability_score"]) for row in rows]
    breach_count = sum(1 for row in rows if bool(row["threshold_breach"]))

    return [
        {"metric": "final_resource_stock", "value": round(resource_values[-1], 6)},
        {"metric": "minimum_resource_stock", "value": round(min(resource_values), 6)},
        {"metric": "average_resource_pressure", "value": round(mean(pressure_values), 6)},
        {"metric": "average_policy_response", "value": round(mean(response_values), 6)},
        {"metric": "final_public_trust", "value": round(trust_values[-1], 6)},
        {"metric": "average_implementation_capacity", "value": round(mean(capacity_values), 6)},
        {"metric": "average_governance_delay", "value": round(mean(delay_values), 6)},
        {"metric": "threshold_breach_count", "value": breach_count},
        {"metric": "average_sustainability_score", "value": round(mean(score_values), 6)},
        {"metric": "minimum_sustainability_score", "value": round(min(score_values), 6)},
    ]


def interpret(summary_rows: list[dict[str, object]]) -> str:
    metrics = {str(row["metric"]): float(row["value"]) for row in summary_rows}

    if metrics["threshold_breach_count"] > 0:
        return "redesign_strategy_due_to_resource_threshold_breach"
    if metrics["final_resource_stock"] < 45.0:
        return "strengthen_adaptive_response_before_resource_stock_declines"
    if metrics["final_public_trust"] < 45.0:
        return "improve_legitimacy_participation_and_distributional_support"
    if metrics["average_governance_delay"] > 8.0:
        return "reduce_governance_delay_and_increase_implementation_capacity"
    return "continue_strategy_with_monitoring_and_adaptive_review"


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
    rows = simulate_sustainability_system()
    summary_rows = summarize(rows)
    recommendation = interpret(summary_rows)
    parameters = load_parameters()

    write_csv(TABLES / "sustainability_system_timeseries.csv", rows)
    write_csv(TABLES / "sustainability_system_summary.csv", summary_rows)

    write_json(
        RECORDS / "sustainability_decision_record.json",
        {
            "article": "Decision Science in Sustainability",
            "decision_context": "Simulating resource pressure, regeneration, adaptive policy response, trust, capacity, and governance delay.",
            "parameters": parameters,
            "summary_metrics": summary_rows,
            "recommendation": recommendation,
            "modeling_principles": [
                "Sustainability decisions are multi-objective, dynamic, uncertain, and distributional.",
                "Resource viability depends on extraction, regeneration, pressure, and adaptive response.",
                "Threshold breaches require stronger action than ordinary trade-off balancing.",
                "Public trust and implementation capacity shape whether sustainability policy can work in practice.",
                "Decision records should preserve assumptions, thresholds, trade-offs, stakeholder concerns, and revision triggers."
            ],
        },
    )

    print("Decision science in sustainability simulation complete.")
    print(TABLES / "sustainability_system_timeseries.csv")
    print(TABLES / "sustainability_system_summary.csv")
    print(RECORDS / "sustainability_decision_record.json")


if __name__ == "__main__":
    main()
