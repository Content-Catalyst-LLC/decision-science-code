#!/usr/bin/env python3
"""
Decision Science in Public Policy workflow.

Simulates policy uptake, feedback quality, implementation capacity,
public trust, implementation drift, and decision-record export.

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


def simulate_policy_system() -> list[dict[str, object]]:
    parameters = load_parameters()
    random.seed(int(parameters["random_seed"]))

    time_steps = int(parameters["time_steps"])
    uptake = parameters["initial_uptake"]
    feedback_quality = parameters["initial_feedback_quality"]
    implementation_drift = parameters["initial_implementation_drift"]
    implementation_capacity = parameters["initial_implementation_capacity"]
    public_trust = parameters["initial_public_trust"]

    rows: list[dict[str, object]] = []

    for time in range(1, time_steps + 1):
        uptake_change = (
            random.gauss(1.30, 0.90)
            + 0.040 * feedback_quality
            + 0.020 * public_trust
            - 0.050 * implementation_drift
        )

        feedback_change = (
            random.gauss(0.60, 0.40)
            + 0.010 * uptake
            + 0.020 * implementation_capacity
            - 0.015 * implementation_drift
        )

        drift_change = (
            random.gauss(0.40, 0.50)
            - 0.030 * feedback_quality
            - 0.020 * implementation_capacity
        )

        capacity_change = (
            random.gauss(0.35, 0.20)
            + 0.015 * feedback_quality
            - 0.020 * implementation_drift
        )

        trust_change = (
            random.gauss(0.10, 0.35)
            + 0.020 * feedback_quality
            - 0.040 * implementation_drift
        )

        uptake = max(0.0, uptake + uptake_change)
        feedback_quality = max(0.0, feedback_quality + feedback_change)
        implementation_drift = max(0.0, implementation_drift + drift_change)
        implementation_capacity = max(0.0, implementation_capacity + capacity_change)
        public_trust = max(0.0, min(100.0, public_trust + trust_change))

        policy_effectiveness = (
            0.30 * uptake
            + 0.22 * feedback_quality
            + 0.22 * implementation_capacity
            + 0.16 * public_trust
            - 0.20 * implementation_drift
        )

        rows.append({
            "time": time,
            "uptake": round(uptake, 6),
            "feedback_quality": round(feedback_quality, 6),
            "implementation_drift": round(implementation_drift, 6),
            "implementation_capacity": round(implementation_capacity, 6),
            "public_trust": round(public_trust, 6),
            "policy_effectiveness": round(policy_effectiveness, 6),
        })

    return rows


def summarize(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    uptake_values = [float(row["uptake"]) for row in rows]
    feedback_values = [float(row["feedback_quality"]) for row in rows]
    drift_values = [float(row["implementation_drift"]) for row in rows]
    capacity_values = [float(row["implementation_capacity"]) for row in rows]
    trust_values = [float(row["public_trust"]) for row in rows]
    effectiveness_values = [float(row["policy_effectiveness"]) for row in rows]

    return [
        {"metric": "final_uptake", "value": round(uptake_values[-1], 6)},
        {"metric": "average_feedback_quality", "value": round(mean(feedback_values), 6)},
        {"metric": "final_implementation_drift", "value": round(drift_values[-1], 6)},
        {"metric": "average_implementation_capacity", "value": round(mean(capacity_values), 6)},
        {"metric": "final_public_trust", "value": round(trust_values[-1], 6)},
        {"metric": "average_policy_effectiveness", "value": round(mean(effectiveness_values), 6)},
        {"metric": "minimum_policy_effectiveness", "value": round(min(effectiveness_values), 6)},
        {"metric": "maximum_policy_effectiveness", "value": round(max(effectiveness_values), 6)},
    ]


def interpret(summary_rows: list[dict[str, object]]) -> str:
    metrics = {str(row["metric"]): float(row["value"]) for row in summary_rows}

    if metrics["final_implementation_drift"] > 15.0:
        return "review_policy_due_to_high_implementation_drift"
    if metrics["final_public_trust"] < 45.0:
        return "strengthen_legitimacy_engagement_and_public_feedback"
    if metrics["minimum_policy_effectiveness"] < 20.0:
        return "redesign_policy_delivery_and_monitoring"
    return "continue_policy_with_adaptive_monitoring_and_review"


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
    rows = simulate_policy_system()
    summary_rows = summarize(rows)
    recommendation = interpret(summary_rows)
    parameters = load_parameters()

    write_csv(TABLES / "public_policy_implementation_timeseries.csv", rows)
    write_csv(TABLES / "public_policy_implementation_summary.csv", summary_rows)

    write_json(
        RECORDS / "public_policy_decision_record.json",
        {
            "article": "Decision Science in Public Policy",
            "decision_context": "Simulating policy uptake, feedback quality, implementation capacity, public trust, and implementation drift.",
            "parameters": parameters,
            "summary_metrics": summary_rows,
            "recommendation": recommendation,
            "modeling_principles": [
                "Public policy decisions are multi-objective, institutional, and distributional.",
                "Policy effectiveness depends on implementation capacity and public trust.",
                "Feedback quality can reduce implementation drift over time.",
                "Decision records should preserve evidence, assumptions, trade-offs, stakeholder concerns, and revision triggers.",
                "Public policy decision science should support accountable judgment, not technocratic closure."
            ],
        },
    )

    print("Decision science in public policy simulation complete.")
    print(TABLES / "public_policy_implementation_timeseries.csv")
    print(TABLES / "public_policy_implementation_summary.csv")
    print(RECORDS / "public_policy_decision_record.json")


if __name__ == "__main__":
    main()
