#!/usr/bin/env python3
"""
Path Dependence, Lock-In, and Decision Timing workflow.

Simulates switching-cost accumulation, lock-in risk, option-value decay,
timing review, and decision-record export.

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


def simulate_path_dependence() -> list[dict[str, object]]:
    parameters = load_parameters()
    random.seed(int(parameters["random_seed"]))

    time_steps = int(parameters["time_steps"])
    investment = parameters["initial_investment"]
    network_dependence = parameters["initial_network_dependence"]
    institutional_routine = parameters["initial_institutional_routine"]
    option_value = parameters["initial_option_value"]
    lock_in_threshold = parameters["lock_in_threshold"]

    rows: list[dict[str, object]] = []

    for time in range(1, time_steps + 1):
        investment_growth = max(0.0, random.gauss(0.018, 0.006))
        network_growth = max(0.0, random.gauss(0.016, 0.007))
        routine_growth = max(0.0, random.gauss(0.014, 0.005))
        option_decay = max(0.0, random.gauss(0.010, 0.004))

        investment = min(1.0, investment + investment_growth)
        network_dependence = min(1.0, network_dependence + network_growth + 0.015 * investment)
        institutional_routine = min(1.0, institutional_routine + routine_growth + 0.010 * network_dependence)
        option_value = max(0.0, option_value - option_decay - 0.006 * institutional_routine)

        switching_cost = (
            0.36 * investment +
            0.34 * network_dependence +
            0.30 * institutional_routine
        )

        lock_in_risk = (
            0.42 * switching_cost +
            0.28 * institutional_routine +
            0.20 * network_dependence -
            0.10 * option_value
        )

        review_trigger = lock_in_risk >= lock_in_threshold or option_value <= 0.35

        rows.append({
            "time": time,
            "investment": round(investment, 6),
            "network_dependence": round(network_dependence, 6),
            "institutional_routine": round(institutional_routine, 6),
            "option_value": round(option_value, 6),
            "switching_cost": round(switching_cost, 6),
            "lock_in_risk": round(lock_in_risk, 6),
            "review_trigger": review_trigger,
        })

    return rows


def summarize(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    switching_costs = [float(row["switching_cost"]) for row in rows]
    lock_in_risks = [float(row["lock_in_risk"]) for row in rows]
    option_values = [float(row["option_value"]) for row in rows]
    review_rows = [row for row in rows if bool(row["review_trigger"])]

    return [
        {"metric": "final_switching_cost", "value": round(switching_costs[-1], 6)},
        {"metric": "peak_switching_cost", "value": round(max(switching_costs), 6)},
        {"metric": "average_switching_cost", "value": round(mean(switching_costs), 6)},
        {"metric": "final_lock_in_risk", "value": round(lock_in_risks[-1], 6)},
        {"metric": "peak_lock_in_risk", "value": round(max(lock_in_risks), 6)},
        {"metric": "final_option_value", "value": round(option_values[-1], 6)},
        {"metric": "minimum_option_value", "value": round(min(option_values), 6)},
        {"metric": "review_trigger_count", "value": len(review_rows)},
        {"metric": "review_trigger_rate", "value": round(len(review_rows) / len(rows), 6)},
    ]


def interpret(summary_rows: list[dict[str, object]]) -> str:
    metrics = {str(row["metric"]): float(row["value"]) for row in summary_rows}

    if metrics["review_trigger_rate"] > 0.25:
        return "redesign_path_before_lock_in_deepens"
    if metrics["final_option_value"] < 0.35:
        return "restore_option_value_and_define_exit_path"
    if metrics["final_switching_cost"] > 0.70:
        return "audit_switching_costs_and_stage_transition"
    return "continue_with_monitoring_and_timing_review"


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
    rows = simulate_path_dependence()
    summary_rows = summarize(rows)
    recommendation = interpret(summary_rows)
    parameters = load_parameters()

    write_csv(TABLES / "path_dependence_lock_in_timeseries.csv", rows)
    write_csv(TABLES / "path_dependence_lock_in_summary.csv", summary_rows)

    write_json(
        RECORDS / "path_dependence_decision_record.json",
        {
            "article": "Path Dependence, Lock-In, and Decision Timing",
            "decision_context": "Simulating switching-cost accumulation, lock-in risk, option-value decline, and timing review.",
            "parameters": parameters,
            "summary_metrics": summary_rows,
            "recommendation": recommendation,
            "modeling_principles": [
                "Earlier choices can change the future choice set.",
                "Switching costs can accumulate through investment, network dependence, and institutional routine.",
                "Delay can reduce option value even when no formal decision is made.",
                "Lock-in risk should trigger review before escape becomes prohibitively costly.",
                "Decision records should preserve timing assumptions, exit paths, and lock-in risks."
            ],
        },
    )

    print("Path dependence, lock-in, and decision timing simulation complete.")
    print(TABLES / "path_dependence_lock_in_timeseries.csv")
    print(TABLES / "path_dependence_lock_in_summary.csv")
    print(RECORDS / "path_dependence_decision_record.json")


if __name__ == "__main__":
    main()
