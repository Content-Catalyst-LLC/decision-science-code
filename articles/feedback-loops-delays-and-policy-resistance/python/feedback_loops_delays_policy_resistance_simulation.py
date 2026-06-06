#!/usr/bin/env python3
"""
Feedback Loops, Delays, and Policy Resistance workflow.

Simulates reinforcing pressure, balancing correction, delayed policy effects,
resistance, threshold risk, and decision-record export.

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


def simulate_policy_dynamics() -> list[dict[str, object]]:
    parameters = load_parameters()
    random.seed(RANDOM_SEED)

    time_steps = int(parameters["time_steps"])
    target_state = parameters["target_state"]
    delay = int(parameters["delay"])
    threshold_risk_level = parameters["threshold_risk_level"]

    system_state = parameters["initial_system_state"]
    policy_signal = parameters["initial_policy_signal"]
    resistance = parameters["initial_resistance"]
    policy_history = [policy_signal]

    rows: list[dict[str, object]] = []

    for time in range(1, time_steps + 1):
        delayed_index = max(0, len(policy_history) - delay)
        delayed_policy_signal = policy_history[delayed_index]

        reinforcing_effect = 0.08 * system_state
        balancing_effect = 0.14 * delayed_policy_signal
        resistance_effect = 0.10 * resistance
        disturbance = random.gauss(0.0, 1.2)

        next_system_state = max(
            0.0,
            system_state + reinforcing_effect - balancing_effect + resistance_effect + disturbance
        )

        next_policy_signal = max(
            0.0,
            policy_signal + 0.06 * (target_state - system_state)
        )

        next_resistance = max(
            0.0,
            resistance + 0.04 * policy_signal - 0.02 * resistance
        )

        threshold_breach = next_system_state >= threshold_risk_level

        rows.append({
            "time": time,
            "system_state": round(next_system_state, 6),
            "policy_signal": round(next_policy_signal, 6),
            "delayed_policy_signal": round(delayed_policy_signal, 6),
            "resistance": round(next_resistance, 6),
            "reinforcing_effect": round(reinforcing_effect, 6),
            "balancing_effect": round(balancing_effect, 6),
            "resistance_effect": round(resistance_effect, 6),
            "disturbance": round(disturbance, 6),
            "threshold_breach": threshold_breach,
        })

        system_state = next_system_state
        policy_signal = next_policy_signal
        resistance = next_resistance
        policy_history.append(policy_signal)

    return rows


def summarize(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    system_values = [float(row["system_state"]) for row in rows]
    policy_values = [float(row["policy_signal"]) for row in rows]
    resistance_values = [float(row["resistance"]) for row in rows]
    threshold_breaches = [row for row in rows if bool(row["threshold_breach"])]

    return [
        {"metric": "final_system_state", "value": round(system_values[-1], 6)},
        {"metric": "peak_system_state", "value": round(max(system_values), 6)},
        {"metric": "average_system_state", "value": round(mean(system_values), 6)},
        {"metric": "average_policy_signal", "value": round(mean(policy_values), 6)},
        {"metric": "average_resistance", "value": round(mean(resistance_values), 6)},
        {"metric": "final_resistance", "value": round(resistance_values[-1], 6)},
        {"metric": "threshold_breach_count", "value": len(threshold_breaches)},
        {"metric": "threshold_breach_rate", "value": round(len(threshold_breaches) / len(rows), 6)},
    ]


def interpret(summary_rows: list[dict[str, object]]) -> str:
    metrics = {str(row["metric"]): float(row["value"]) for row in summary_rows}
    threshold_risk_level = load_parameters()["threshold_risk_level"]

    if metrics["threshold_breach_rate"] > 0.20:
        return "redesign_policy_due_to_threshold_breach"
    if metrics["final_resistance"] > metrics["average_policy_signal"]:
        return "review_policy_resistance_and_counter_response"
    if metrics["peak_system_state"] > threshold_risk_level:
        return "strengthen_delay_controls_and_monitoring"
    return "continue_with_feedback_monitoring_and_structured_review"


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
    rows = simulate_policy_dynamics()
    summary_rows = summarize(rows)
    recommendation = interpret(summary_rows)
    parameters = load_parameters()

    write_csv(TABLES / "feedback_delay_policy_timeseries.csv", rows)
    write_csv(TABLES / "feedback_delay_policy_summary.csv", summary_rows)

    write_json(
        RECORDS / "feedback_delay_policy_decision_record.json",
        {
            "article": "Feedback Loops, Delays, and Policy Resistance",
            "decision_context": "Simulating reinforcing pressure, balancing correction, delayed policy effects, resistance, and threshold risk.",
            "random_seed": RANDOM_SEED,
            "parameters": parameters,
            "summary_metrics": summary_rows,
            "recommendation": recommendation,
            "modeling_principles": [
                "Feedback loops can amplify or counteract policy effects.",
                "Delayed responses can cause overcorrection, false confidence, or premature abandonment.",
                "Policy resistance should be modeled as a system response, not only an implementation failure.",
                "Threshold breaches should trigger structured review.",
                "Decision records should preserve feedback assumptions, delays, resistance risks, and monitoring triggers."
            ],
        },
    )

    print("Feedback, delay, and policy resistance simulation complete.")
    print(TABLES / "feedback_delay_policy_timeseries.csv")
    print(TABLES / "feedback_delay_policy_summary.csv")
    print(RECORDS / "feedback_delay_policy_decision_record.json")


if __name__ == "__main__":
    main()
