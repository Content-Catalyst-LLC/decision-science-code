#!/usr/bin/env python3
"""
Cascading Risk and Systemic Decision Failure workflow.

Simulates threshold-based cascading failure across an interdependent
network, including stress propagation, buffer depletion, systemic loss,
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

NODES = {
    "Energy": {"threshold": 0.72, "criticality": 0.22, "buffer": 0.58},
    "Water": {"threshold": 0.68, "criticality": 0.18, "buffer": 0.54},
    "Transport": {"threshold": 0.70, "criticality": 0.16, "buffer": 0.50},
    "Healthcare": {"threshold": 0.66, "criticality": 0.20, "buffer": 0.46},
    "Communications": {"threshold": 0.64, "criticality": 0.14, "buffer": 0.52},
    "Public Administration": {"threshold": 0.62, "criticality": 0.10, "buffer": 0.44},
}

DEPENDENCIES = {
    "Energy": {"Communications": 0.18, "Transport": 0.10},
    "Water": {"Energy": 0.28, "Communications": 0.08},
    "Transport": {"Energy": 0.20, "Communications": 0.12},
    "Healthcare": {"Energy": 0.24, "Water": 0.18, "Transport": 0.12, "Communications": 0.14},
    "Communications": {"Energy": 0.22},
    "Public Administration": {"Communications": 0.18, "Energy": 0.10, "Transport": 0.08},
}


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def load_parameters() -> dict[str, float]:
    return {
        row["parameter"]: float(row["value"])
        for row in read_csv_dicts(DATA / "synthetic_system_parameters.csv")
    }


def simulate_cascade() -> list[dict[str, object]]:
    parameters = load_parameters()
    random.seed(int(parameters["random_seed"]))

    time_steps = int(parameters["time_steps"])
    initial_stress = parameters["initial_stress"]
    external_shock_time = int(parameters["external_shock_time"])
    external_shock_size = parameters["external_shock_size"]

    states = {
        node: {
            "stress": initial_stress,
            "buffer": params["buffer"],
            "failed": False,
        }
        for node, params in NODES.items()
    }

    rows: list[dict[str, object]] = []

    for time in range(1, time_steps + 1):
        external_shock = external_shock_size if time == external_shock_time else 0.0
        previous_failed = {node: states[node]["failed"] for node in NODES}

        for node, params in NODES.items():
            dependency_stress = 0.0
            for source, weight in DEPENDENCIES.get(node, {}).items():
                if previous_failed[source]:
                    dependency_stress += weight

            random_noise = max(0.0, random.gauss(0.015, 0.01))
            recovery = 0.025 if not states[node]["failed"] else 0.010

            stress = max(
                0.0,
                states[node]["stress"] + dependency_stress + external_shock + random_noise - recovery
            )

            buffer = max(
                0.0,
                states[node]["buffer"] - 0.08 * stress + 0.015
            )

            effective_stress = stress + max(0.0, 0.40 - buffer)
            failed = effective_stress >= params["threshold"]

            states[node] = {
                "stress": stress,
                "buffer": buffer,
                "failed": failed,
            }

        systemic_loss = sum(
            NODES[node]["criticality"] for node in NODES if states[node]["failed"]
        )

        for node in NODES:
            rows.append({
                "time": time,
                "node": node,
                "stress": round(states[node]["stress"], 6),
                "buffer": round(states[node]["buffer"], 6),
                "failed": states[node]["failed"],
                "systemic_loss": round(systemic_loss, 6),
                "external_shock": round(external_shock, 6),
            })

    return rows


def summarize(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    times = sorted({int(row["time"]) for row in rows})
    systemic_loss_by_time = []

    for time in times:
        time_rows = [row for row in rows if int(row["time"]) == time]
        systemic_loss_by_time.append(float(time_rows[0]["systemic_loss"]))

    failed_rows = [row for row in rows if bool(row["failed"])]
    failure_times = sorted({int(row["time"]) for row in failed_rows})

    node_failure_counts: dict[str, int] = {}
    for row in failed_rows:
        node = str(row["node"])
        node_failure_counts[node] = node_failure_counts.get(node, 0) + 1

    summary = [
        {"metric": "peak_systemic_loss", "value": round(max(systemic_loss_by_time), 6)},
        {"metric": "average_systemic_loss", "value": round(mean(systemic_loss_by_time), 6)},
        {"metric": "failure_time_count", "value": len(failure_times)},
        {"metric": "total_failed_node_periods", "value": len(failed_rows)},
        {"metric": "maximum_node_failure_count", "value": max(node_failure_counts.values()) if node_failure_counts else 0},
    ]

    for node in sorted(NODES):
        summary.append({
            "metric": f"failed_periods_{node}",
            "value": node_failure_counts.get(node, 0),
        })

    return summary


def interpret(summary_rows: list[dict[str, object]]) -> str:
    metrics = {str(row["metric"]): float(row["value"]) for row in summary_rows}
    redesign_threshold = load_parameters()["systemic_loss_redesign_threshold"]

    if metrics["peak_systemic_loss"] >= redesign_threshold:
        return "redesign_dependencies_and_add_containment_before_systemic_failure"
    if metrics["failure_time_count"] >= 5:
        return "increase_buffer_capacity_and_define_escalation_triggers"
    if metrics["total_failed_node_periods"] >= 8:
        return "review_common_mode_exposure_and_recovery_capacity"
    return "continue_monitoring_with_targeted_dependency_review"


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
    rows = simulate_cascade()
    summary_rows = summarize(rows)
    recommendation = interpret(summary_rows)
    parameters = load_parameters()

    write_csv(TABLES / "cascading_failure_timeseries.csv", rows)
    write_csv(TABLES / "cascading_failure_summary.csv", summary_rows)

    write_json(
        RECORDS / "cascading_risk_decision_record.json",
        {
            "article": "Cascading Risk and Systemic Decision Failure",
            "decision_context": "Simulating threshold-based cascading failure across an interdependent network.",
            "parameters": parameters,
            "nodes": NODES,
            "dependencies": DEPENDENCIES,
            "summary_metrics": summary_rows,
            "recommendation": recommendation,
            "modeling_principles": [
                "Cascading risk depends on dependency structure, not only initial shock size.",
                "Threshold failures can propagate when neighboring systems fail.",
                "Buffers and recovery capacity reduce systemic loss.",
                "Common-mode exposure can defeat apparent diversification.",
                "Decision records should preserve dependencies, thresholds, monitoring indicators, and containment plans."
            ],
        },
    )

    print("Cascading risk and systemic decision failure simulation complete.")
    print(TABLES / "cascading_failure_timeseries.csv")
    print(TABLES / "cascading_failure_summary.csv")
    print(RECORDS / "cascading_risk_decision_record.json")


if __name__ == "__main__":
    main()
