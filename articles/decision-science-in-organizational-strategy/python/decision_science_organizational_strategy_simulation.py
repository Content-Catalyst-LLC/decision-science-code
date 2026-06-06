#!/usr/bin/env python3
"""
Decision Science in Organizational Strategy workflow.

Simulates strategic review cycles under uncertainty, disruption,
assumption drift, governance support, and adaptive learning.

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

STRATEGIES = {
    "Scale Existing Core": {
        "base_return": 1.2,
        "volatility": 1.8,
        "adaptability": 0.42,
        "resilience": 0.72,
        "capability_fit": 0.86,
        "governance_support": 0.78,
    },
    "Modular Expansion": {
        "base_return": 1.4,
        "volatility": 2.0,
        "adaptability": 0.84,
        "resilience": 0.78,
        "capability_fit": 0.72,
        "governance_support": 0.70,
    },
    "High-Risk Market Entry": {
        "base_return": 2.0,
        "volatility": 4.2,
        "adaptability": 0.48,
        "resilience": 0.36,
        "capability_fit": 0.44,
        "governance_support": 0.46,
    },
    "Capability Renewal": {
        "base_return": 1.5,
        "volatility": 2.4,
        "adaptability": 0.90,
        "resilience": 0.74,
        "capability_fit": 0.70,
        "governance_support": 0.66,
    },
    "Resilience-Oriented Redesign": {
        "base_return": 1.1,
        "volatility": 1.6,
        "adaptability": 0.82,
        "resilience": 0.88,
        "capability_fit": 0.76,
        "governance_support": 0.80,
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


def simulate_strategy(
    name: str,
    config: dict[str, float],
    time_steps: int,
    review_trigger_value: float,
    drift_trigger: float,
) -> list[dict[str, object]]:
    strategic_value = 100.0
    assumption_drift = 0.0
    rows: list[dict[str, object]] = []

    for time in range(1, time_steps + 1):
        shock = random.gauss(0.0, config["volatility"])
        disruption_event = random.random() < 0.14

        disruption_penalty = 0.0
        if disruption_event:
            disruption_penalty = random.uniform(2.5, 8.0) * (1.0 - config["resilience"])
            assumption_drift += random.uniform(0.04, 0.12)

        learning_adjustment = (
            0.55 * config["adaptability"]
            + 0.35 * config["resilience"]
            + 0.20 * config["governance_support"]
            - 0.30 * assumption_drift
        )

        growth_rate = (
            config["base_return"]
            + shock
            + learning_adjustment
            - disruption_penalty
        )

        strategic_value = max(35.0, strategic_value * (1.0 + growth_rate / 100.0))

        assumption_drift = max(
            0.0,
            min(
                1.0,
                assumption_drift
                + random.gauss(0.01, 0.02)
                - 0.025 * config["adaptability"]
                - 0.015 * config["governance_support"]
            )
        )

        review_required = (
            strategic_value < review_trigger_value
            or assumption_drift > drift_trigger
            or config["capability_fit"] < 0.55
            or config["governance_support"] < 0.55
        )

        rows.append({
            "strategy": name,
            "time": time,
            "strategic_value": round(strategic_value, 6),
            "shock": round(shock, 6),
            "disruption_event": disruption_event,
            "disruption_penalty": round(disruption_penalty, 6),
            "assumption_drift": round(assumption_drift, 6),
            "learning_adjustment": round(learning_adjustment, 6),
            "review_required": review_required,
        })

    return rows


def simulate_all() -> list[dict[str, object]]:
    params = load_parameters()
    random.seed(int(params["random_seed"]))

    rows: list[dict[str, object]] = []
    for name, config in STRATEGIES.items():
        rows.extend(
            simulate_strategy(
                name,
                config,
                time_steps=int(params["time_steps"]),
                review_trigger_value=params["review_trigger_value"],
                drift_trigger=params["assumption_drift_trigger"],
            )
        )

    return rows


def summarize(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    strategies = sorted({str(row["strategy"]) for row in rows})
    summary: list[dict[str, object]] = []

    for strategy in strategies:
        s_rows = [row for row in rows if row["strategy"] == strategy]
        values = [float(row["strategic_value"]) for row in s_rows]
        drift_values = [float(row["assumption_drift"]) for row in s_rows]
        review_count = sum(1 for row in s_rows if bool(row["review_required"]))
        disruption_count = sum(1 for row in s_rows if bool(row["disruption_event"]))

        summary.append({
            "strategy": strategy,
            "final_value": round(values[-1], 6),
            "minimum_value": round(min(values), 6),
            "average_value": round(mean(values), 6),
            "maximum_assumption_drift": round(max(drift_values), 6),
            "average_assumption_drift": round(mean(drift_values), 6),
            "disruption_event_count": disruption_count,
            "review_required_count": review_count,
            "review_flag": "review" if review_count > 0 else "acceptable",
        })

    summary.sort(key=lambda row: (float(row["final_value"]), float(row["minimum_value"])), reverse=True)
    return summary


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
    params = load_parameters()
    rows = simulate_all()
    summary_rows = summarize(rows)

    write_csv(TABLES / "organizational_strategy_timeseries.csv", rows)
    write_csv(TABLES / "organizational_strategy_summary.csv", summary_rows)

    write_json(
        RECORDS / "organizational_strategy_decision_record.json",
        {
            "article": "Decision Science in Organizational Strategy",
            "decision_context": "Simulating strategic review cycles under uncertainty, disruption, assumption drift, and adaptive learning.",
            "parameters": params,
            "summary_metrics": summary_rows,
            "modeling_principles": [
                "Strategy is a decision system, not only a plan document.",
                "Strategic quality depends on uncertainty classification, alternatives, resources, governance, and learning.",
                "High upside can be strategically weak when downside resilience, capability fit, and governance support are low.",
                "Assumption drift should trigger review before performance collapse becomes visible.",
                "Decision records should preserve assumptions, alternatives, dissent, trade-offs, and revision triggers."
            ],
        },
    )

    print("Decision science in organizational strategy simulation complete.")
    print(TABLES / "organizational_strategy_timeseries.csv")
    print(TABLES / "organizational_strategy_summary.csv")
    print(RECORDS / "organizational_strategy_decision_record.json")


if __name__ == "__main__":
    main()
