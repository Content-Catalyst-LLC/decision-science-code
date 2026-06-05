#!/usr/bin/env python3
"""
Adaptive Decision Quality Simulation

Compares strategies across:
- short-term gain
- uncertainty exposure
- robustness
- learning capacity
- reversibility
- evidence quality
- decision-record completeness

Uses only the Python standard library.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import csv
import json
import random
from statistics import mean, pstdev

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
DATA = ARTICLE_ROOT / "data"
TABLES = ARTICLE_ROOT / "outputs" / "tables"
RECORDS = ARTICLE_ROOT / "outputs" / "decision_records"


@dataclass(frozen=True)
class Strategy:
    name: str
    base_gain: float
    uncertainty_load: float
    robustness: float
    learning_capacity: float
    reversibility: float
    evidence_quality: float
    decision_record_completeness: float


@dataclass(frozen=True)
class Environment:
    name: str
    probability: float
    shock_mean: float
    shock_sd: float
    system_stress: float
    learning_opportunity: float


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def load_strategies() -> list[Strategy]:
    rows = read_csv_dicts(DATA / "synthetic_strategy_parameters.csv")
    return [
        Strategy(
            row["strategy"],
            float(row["base_gain"]),
            float(row["uncertainty_load"]),
            float(row["robustness"]),
            float(row["learning_capacity"]),
            float(row["reversibility"]),
            float(row["evidence_quality"]),
            float(row["decision_record_completeness"]),
        )
        for row in rows
    ]


def load_environments() -> list[Environment]:
    rows = read_csv_dicts(DATA / "synthetic_uncertainty_scenarios.csv")
    environments = [
        Environment(
            row["scenario"],
            float(row["probability"]),
            float(row["shock_mean"]),
            float(row["shock_sd"]),
            float(row["system_stress"]),
            float(row["learning_opportunity"]),
        )
        for row in rows
    ]
    validate_probabilities(environments)
    return environments


def validate_probabilities(environments: list[Environment]) -> None:
    total = sum(environment.probability for environment in environments)
    if abs(total - 1.0) > 1e-9:
        raise ValueError(f"Environment probabilities must sum to 1. Current sum: {total}")


def weighted_environment(environments: list[Environment], rng: random.Random) -> Environment:
    draw = rng.random()
    cumulative = 0.0
    for environment in environments:
        cumulative += environment.probability
        if draw <= cumulative:
            return environment
    return environments[-1]


def simulate_strategy(strategy: Strategy, environments: list[Environment], cycles: int, seed: int) -> list[dict[str, object]]:
    rng = random.Random(seed)
    value = 100.0
    belief_quality = strategy.evidence_quality
    rows: list[dict[str, object]] = []

    for cycle in range(1, cycles + 1):
        environment = weighted_environment(environments, rng)
        shock = rng.gauss(environment.shock_mean, environment.shock_sd)

        stress_penalty = environment.system_stress * (1.0 - strategy.robustness) * 4.0
        uncertainty_penalty = strategy.uncertainty_load * abs(shock) * 0.35
        learning_credit = strategy.learning_capacity * environment.learning_opportunity * 2.0
        reversibility_credit = strategy.reversibility * max(0.0, -shock) * 0.30
        record_credit = strategy.decision_record_completeness * 0.30

        growth_rate = (
            strategy.base_gain
            + shock
            - stress_penalty
            - uncertainty_penalty
            + learning_credit
            + reversibility_credit
            + record_credit
        )

        value = max(35.0, value * (1.0 + growth_rate / 100.0))

        belief_quality = min(
            1.0,
            belief_quality
            + 0.02 * strategy.learning_capacity * environment.learning_opportunity
            + 0.01 * strategy.decision_record_completeness,
        )

        trigger_review = (
            value < 75.0
            or environment.system_stress > 0.70
            or belief_quality < 0.60
        )

        rows.append({
            "cycle": cycle,
            "strategy": strategy.name,
            "environment": environment.name,
            "value": round(value, 4),
            "growth_rate": round(growth_rate, 4),
            "belief_quality": round(belief_quality, 4),
            "trigger_review": trigger_review,
        })

    return rows


def summarize(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    strategies = sorted({str(row["strategy"]) for row in rows})
    output: list[dict[str, object]] = []

    for strategy in strategies:
        strategy_rows = [row for row in rows if row["strategy"] == strategy]
        values = [float(row["value"]) for row in strategy_rows]
        growth = [float(row["growth_rate"]) for row in strategy_rows]
        reviews = [row["trigger_review"] for row in strategy_rows]

        output.append({
            "strategy": strategy,
            "final_value": round(values[-1], 4),
            "minimum_value": round(min(values), 4),
            "average_value": round(mean(values), 4),
            "value_sd": round(pstdev(values), 4),
            "average_growth_rate": round(mean(growth), 4),
            "review_trigger_frequency": round(sum(1 for item in reviews if item) / len(reviews), 4),
        })

    return sorted(output, key=lambda row: float(row["final_value"]), reverse=True)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"No rows to write: {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_decision_record(path: Path, summary_rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "article": "Core Principles of Decision Science",
        "decision_context": "Adaptive decision-quality simulation under uncertainty.",
        "selected_strategy": summary_rows[0]["strategy"],
        "interpretation": "The selected strategy has the strongest simulated performance across uncertainty, learning, robustness, and review-trigger conditions.",
        "modeling_principles": [
            "Define the decision before modeling options.",
            "Represent uncertainty honestly.",
            "Surface trade-offs explicitly.",
            "Use sensitivity and scenario comparison.",
            "Account for systems consequences.",
            "Prefer robustness and adaptability under deep uncertainty.",
            "Document decision records for accountability and learning.",
            "Treat computational models as supports for judgment.",
        ],
        "summary": summary_rows,
        "review_triggers": [
            "performance falls below threshold",
            "system stress rises above tolerance",
            "belief quality deteriorates",
            "new evidence changes assumptions",
            "trade-off weights are contested",
        ],
    }
    path.write_text(json.dumps(record, indent=2), encoding="utf-8")


def main() -> None:
    strategies = load_strategies()
    environments = load_environments()
    all_rows: list[dict[str, object]] = []

    for index, strategy in enumerate(strategies):
        all_rows.extend(simulate_strategy(strategy, environments, cycles=60, seed=42 + index))

    summary_rows = summarize(all_rows)

    write_csv(TABLES / "adaptive_decision_quality_cycles.csv", all_rows)
    write_csv(TABLES / "adaptive_decision_quality_summary.csv", summary_rows)
    write_decision_record(RECORDS / "core_principles_decision_record.json", summary_rows)

    print("Adaptive decision quality simulation complete.")
    print(TABLES / "adaptive_decision_quality_summary.csv")
    print(RECORDS / "core_principles_decision_record.json")


if __name__ == "__main__":
    main()
