#!/usr/bin/env python3
"""
Adaptive Decision Pathways workflow.

Simulates trigger-based movement across adaptive decision pathways under
changing system stress and option value.

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

PATHWAYS = {
    "baseline_path": {
        "performance": 0.74,
        "flexibility": 0.42,
        "switching_cost": 0.22,
        "fallback_strength": 0.38,
    },
    "moderate_adaptation_path": {
        "performance": 0.76,
        "flexibility": 0.72,
        "switching_cost": 0.34,
        "fallback_strength": 0.68,
    },
    "high_resilience_path": {
        "performance": 0.78,
        "flexibility": 0.84,
        "switching_cost": 0.48,
        "fallback_strength": 0.82,
    },
}


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def load_parameters() -> dict[str, float]:
    return {
        row["parameter"]: float(row["value"])
        for row in read_csv_dicts(DATA / "synthetic_system_parameters.csv")
    }


def simulate_pathway() -> list[dict[str, object]]:
    parameters = load_parameters()
    random.seed(int(parameters["random_seed"]))

    time_steps = int(parameters["time_steps"])
    current_pathway = "baseline_path"
    system_stress = parameters["initial_system_stress"]
    option_value = parameters["initial_option_value"]
    stress_trigger = parameters["stress_trigger"]
    option_value_trigger = parameters["option_value_trigger"]
    pathway_switches = 0

    rows: list[dict[str, object]] = []

    for time in range(1, time_steps + 1):
        risk_growth = max(0.0, random.gauss(0.018, 0.010))
        learning_gain = max(0.0, random.gauss(0.010, 0.004))
        pathway = PATHWAYS[current_pathway]

        stress_reduction = 0.020 * pathway["fallback_strength"] + 0.015 * pathway["flexibility"]
        system_stress = min(1.0, max(0.0, system_stress + risk_growth - stress_reduction))

        option_value = max(
            0.0,
            option_value - 0.010 - 0.012 * pathway["switching_cost"] + 0.010 * pathway["flexibility"]
        )

        trigger_hit = system_stress >= stress_trigger or option_value <= option_value_trigger
        switched = False

        if trigger_hit and current_pathway == "baseline_path":
            current_pathway = "moderate_adaptation_path"
            pathway_switches += 1
            switched = True
        elif trigger_hit and current_pathway == "moderate_adaptation_path":
            current_pathway = "high_resilience_path"
            pathway_switches += 1
            switched = True

        active_pathway = PATHWAYS[current_pathway]
        effective_performance = (
            active_pathway["performance"]
            - 0.25 * system_stress
            + 0.08 * active_pathway["fallback_strength"]
            + 0.04 * learning_gain
        )

        rows.append({
            "time": time,
            "pathway": current_pathway,
            "system_stress": round(system_stress, 6),
            "option_value": round(option_value, 6),
            "effective_performance": round(effective_performance, 6),
            "trigger_hit": trigger_hit,
            "switched": switched,
            "pathway_switches": pathway_switches,
        })

    return rows


def summarize(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    performance_values = [float(row["effective_performance"]) for row in rows]
    stress_values = [float(row["system_stress"]) for row in rows]
    option_values = [float(row["option_value"]) for row in rows]
    switch_count = int(rows[-1]["pathway_switches"])
    trigger_count = sum(1 for row in rows if bool(row["trigger_hit"]))

    return [
        {"metric": "average_performance", "value": round(mean(performance_values), 6)},
        {"metric": "worst_case_performance", "value": round(min(performance_values), 6)},
        {"metric": "final_system_stress", "value": round(stress_values[-1], 6)},
        {"metric": "peak_system_stress", "value": round(max(stress_values), 6)},
        {"metric": "final_option_value", "value": round(option_values[-1], 6)},
        {"metric": "minimum_option_value", "value": round(min(option_values), 6)},
        {"metric": "trigger_count", "value": trigger_count},
        {"metric": "pathway_switch_count", "value": switch_count},
    ]


def interpret(summary_rows: list[dict[str, object]]) -> str:
    metrics = {str(row["metric"]): float(row["value"]) for row in summary_rows}

    if metrics["worst_case_performance"] < 0.55:
        return "redesign_pathway_due_to_low_worst_case_performance"
    if metrics["peak_system_stress"] >= 0.80:
        return "strengthen_triggers_and_shift_to_higher_resilience_pathway"
    if metrics["minimum_option_value"] <= 0.35:
        return "restore_option_value_and_reduce_switching_costs"
    return "continue_monitoring_with_adaptive_review"


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
    rows = simulate_pathway()
    summary_rows = summarize(rows)
    recommendation = interpret(summary_rows)
    parameters = load_parameters()

    write_csv(TABLES / "adaptive_pathway_timeseries.csv", rows)
    write_csv(TABLES / "adaptive_pathway_summary.csv", summary_rows)

    write_json(
        RECORDS / "adaptive_decision_pathway_record.json",
        {
            "article": "Adaptive Decision Pathways",
            "decision_context": "Simulating trigger-based movement across adaptive decision pathways under changing stress and option value.",
            "parameters": parameters,
            "pathways": PATHWAYS,
            "summary_metrics": summary_rows,
            "recommendation": recommendation,
            "modeling_principles": [
                "Adaptive pathways separate initial action from future revision.",
                "Trigger points connect monitoring indicators to decision authority.",
                "Option value can decline when switching costs rise or flexibility erodes.",
                "Fallback strength improves performance under stress.",
                "Decision records should preserve assumptions, thresholds, switching rules, and revision authority."
            ],
        },
    )

    print("Adaptive decision pathways simulation complete.")
    print(TABLES / "adaptive_pathway_timeseries.csv")
    print(TABLES / "adaptive_pathway_summary.csv")
    print(RECORDS / "adaptive_decision_pathway_record.json")


if __name__ == "__main__":
    main()
