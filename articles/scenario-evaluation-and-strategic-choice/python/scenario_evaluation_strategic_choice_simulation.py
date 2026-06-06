#!/usr/bin/env python3
"""
Scenario Evaluation and Strategic Choice simulation.

Simulates repeated strategy performance under scenario volatility,
exports time-series results, summarizes downside exposure, and writes
a scenario evaluation decision record.

Uses only the Python standard library.
"""

from __future__ import annotations

from pathlib import Path
import csv
import json
import random
from statistics import mean, pstdev

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
DATA = ARTICLE_ROOT / "data"
TABLES = ARTICLE_ROOT / "outputs" / "tables"
RECORDS = ARTICLE_ROOT / "outputs" / "decision_records"

STRATEGIES = {
    "Aggressive Expansion": {"base_return": 1.8, "volatility": 4.6, "resilience": 0.4},
    "Balanced Optionality": {"base_return": 1.4, "volatility": 2.8, "resilience": 1.1},
    "Defensive Resilience": {"base_return": 1.0, "volatility": 1.8, "resilience": 1.5},
    "Adaptive Sequencing": {"base_return": 1.5, "volatility": 2.4, "resilience": 1.3},
    "Robust Modular Strategy": {"base_return": 1.3, "volatility": 2.0, "resilience": 1.6},
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
    base_return: float,
    volatility: float,
    resilience: float,
    time_steps: int,
    initial_value: float,
    floor_value: float,
) -> list[dict[str, object]]:
    value = initial_value
    rows: list[dict[str, object]] = []

    for time in range(1, time_steps + 1):
        shock = random.gauss(0.0, volatility)
        adaptive_buffer = resilience * random.uniform(0.4, 1.2)
        growth = base_return + shock + adaptive_buffer
        value = max(floor_value, value * (1.0 + growth / 100.0))

        rows.append({
            "time": time,
            "strategy": name,
            "strategy_value_index": round(value, 6),
            "shock": round(shock, 6),
            "adaptive_buffer": round(adaptive_buffer, 6),
            "growth_rate": round(growth, 6),
        })

    return rows


def simulate_all() -> list[dict[str, object]]:
    parameters = load_parameters()
    random.seed(int(parameters["random_seed"]))

    rows: list[dict[str, object]] = []
    for name, params in STRATEGIES.items():
        rows.extend(
            simulate_strategy(
                name=name,
                base_return=params["base_return"],
                volatility=params["volatility"],
                resilience=params["resilience"],
                time_steps=int(parameters["time_steps"]),
                initial_value=parameters["initial_value"],
                floor_value=parameters["floor_value"],
            )
        )

    return rows


def summarize(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    parameters = load_parameters()
    initial_value = parameters["initial_value"]

    by_strategy: dict[str, list[float]] = {}
    for row in rows:
        by_strategy.setdefault(str(row["strategy"]), []).append(float(row["strategy_value_index"]))

    summary: list[dict[str, object]] = []
    for strategy, values in by_strategy.items():
        final_value = values[-1]
        min_value = min(values)
        max_value = max(values)
        average_value = mean(values)
        volatility = pstdev(values)
        downside_exposure = max(0.0, initial_value - min_value)
        robustness_score = (
            0.34 * (final_value / initial_value)
            + 0.24 * (min_value / initial_value)
            + 0.22 * (average_value / initial_value)
            - 0.10 * (volatility / initial_value)
            - 0.10 * (downside_exposure / initial_value)
        )

        summary.append({
            "strategy": strategy,
            "final_value": round(final_value, 6),
            "minimum_value": round(min_value, 6),
            "maximum_value": round(max_value, 6),
            "average_value": round(average_value, 6),
            "path_volatility": round(volatility, 6),
            "downside_exposure": round(downside_exposure, 6),
            "simulation_robustness_score": round(robustness_score, 6),
        })

    summary = sorted(summary, key=lambda row: float(row["simulation_robustness_score"]), reverse=True)
    for rank, row in enumerate(summary, start=1):
        row["rank"] = rank

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
    rows = simulate_all()
    summary = summarize(rows)
    parameters = load_parameters()

    write_csv(TABLES / "scenario_strategy_volatility_timeseries.csv", rows)
    write_csv(TABLES / "scenario_strategy_volatility_summary.csv", summary)

    write_json(
        RECORDS / "scenario_evaluation_decision_record.json",
        {
            "article": "Scenario Evaluation and Strategic Choice",
            "decision_context": "Simulating strategy performance under repeated scenario volatility and adaptive buffers.",
            "parameters": parameters,
            "strategy_parameters": STRATEGIES,
            "ranked_results": summary,
            "selected_strategy": summary[0]["strategy"],
            "modeling_principles": [
                "Scenario evaluation compares strategies across uncertainty rather than relying on one forecast.",
                "Robust strategies should be judged by downside exposure, threshold performance, and adaptability.",
                "High upside does not always imply defensible strategic choice.",
                "Adaptive buffers and monitoring matter when scenarios evolve over time.",
                "Decision records should preserve scenario assumptions, evaluation rules, and revision triggers."
            ],
        },
    )

    print("Scenario evaluation and strategic choice simulation complete.")
    print(TABLES / "scenario_strategy_volatility_timeseries.csv")
    print(TABLES / "scenario_strategy_volatility_summary.csv")
    print(RECORDS / "scenario_evaluation_decision_record.json")


if __name__ == "__main__":
    main()
