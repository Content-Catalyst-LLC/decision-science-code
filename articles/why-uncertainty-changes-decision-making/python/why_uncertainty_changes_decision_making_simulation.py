#!/usr/bin/env python3
"""
Decision-making under uncertainty simulation.

Compares:
- expected value
- ambiguity-adjusted utility
- minimax regret
- adaptive choice
- robustness diagnostics
- monitoring triggers
- decision-record output

Uses only the Python standard library.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import csv
import json
import math
import random
from statistics import mean, pstdev

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
DATA = ARTICLE_ROOT / "data"
TABLES = ARTICLE_ROOT / "outputs" / "tables"
RECORDS = ARTICLE_ROOT / "outputs" / "decision_records"


@dataclass(frozen=True)
class Scenario:
    name: str
    probability: float
    payoff_multiplier: float
    disruption: float
    model_shift: float
    delay_cost: float


@dataclass(frozen=True)
class Strategy:
    name: str
    base_value: float
    cost: float
    ambiguity_exposure: float
    reversibility: float
    robustness: float
    implementation_capacity: float
    evidence_quality: float
    learning_capacity: float


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def load_scenarios() -> list[Scenario]:
    rows = read_csv_dicts(DATA / "synthetic_scenarios.csv")
    scenarios = [
        Scenario(
            row["scenario"],
            float(row["probability"]),
            float(row["payoff_multiplier"]),
            float(row["disruption"]),
            float(row["model_shift"]),
            float(row["delay_cost"]),
        )
        for row in rows
    ]
    validate_probabilities(scenarios)
    return scenarios


def load_strategies() -> list[Strategy]:
    rows = read_csv_dicts(DATA / "synthetic_strategies.csv")
    return [
        Strategy(
            row["strategy"],
            float(row["base_value"]),
            float(row["cost"]),
            float(row["ambiguity_exposure"]),
            float(row["reversibility"]),
            float(row["robustness"]),
            float(row["implementation_capacity"]),
            float(row["evidence_quality"]),
            float(row["learning_capacity"]),
        )
        for row in rows
    ]


def validate_probabilities(scenarios: list[Scenario]) -> None:
    total = sum(s.probability for s in scenarios)
    if not math.isclose(total, 1.0, abs_tol=1e-9):
        raise ValueError(f"Scenario probabilities must sum to 1. Current sum: {total}")


def utility(value: float, risk_aversion: float = 0.016) -> float:
    return 1.0 - math.exp(-risk_aversion * value)


def payoff(strategy: Strategy, scenario: Scenario) -> float:
    gross_value = strategy.base_value * scenario.payoff_multiplier
    direct_cost = strategy.cost
    disruption_penalty = scenario.disruption * (1.0 - strategy.robustness) * 90.0
    model_shift_penalty = scenario.model_shift * strategy.ambiguity_exposure * 80.0
    implementation_penalty = scenario.disruption * (1.0 - strategy.implementation_capacity) * 45.0
    evidence_penalty = (1.0 - strategy.evidence_quality) * 18.0
    reversibility_credit = strategy.reversibility * scenario.model_shift * 28.0
    learning_credit = strategy.learning_capacity * scenario.delay_cost * 18.0

    return (
        gross_value
        - direct_cost
        - disruption_penalty
        - model_shift_penalty
        - implementation_penalty
        - evidence_penalty
        + reversibility_credit
        + learning_credit
    )


def expected_value(strategy: Strategy, scenarios: list[Scenario]) -> float:
    return sum(s.probability * payoff(strategy, s) for s in scenarios)


def expected_utility(strategy: Strategy, scenarios: list[Scenario]) -> float:
    return sum(s.probability * utility(payoff(strategy, s)) for s in scenarios)


def ambiguity_adjusted_value(
    strategy: Strategy,
    scenarios: list[Scenario],
    ambiguity_lambda: float = 1.5,
) -> float:
    return expected_utility(strategy, scenarios) - ambiguity_lambda * strategy.ambiguity_exposure


def regret_rows(strategies: list[Strategy], scenarios: list[Scenario]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    for scenario in scenarios:
        values = {strategy.name: payoff(strategy, scenario) for strategy in strategies}
        best_value = max(values.values())

        for strategy in strategies:
            strategy_value = values[strategy.name]
            rows.append({
                "scenario": scenario.name,
                "strategy": strategy.name,
                "payoff": round(strategy_value, 4),
                "best_payoff": round(best_value, 4),
                "regret": round(best_value - strategy_value, 4),
            })

    return rows


def maximum_regret(strategy: Strategy, strategies: list[Strategy], scenarios: list[Scenario]) -> float:
    rows = regret_rows(strategies, scenarios)
    return max(float(row["regret"]) for row in rows if row["strategy"] == strategy.name)


def robustness_share(strategy: Strategy, scenarios: list[Scenario], threshold: float = 40.0) -> float:
    return sum(1 for scenario in scenarios if payoff(strategy, scenario) >= threshold) / len(scenarios)


def weighted_choice(scenarios: list[Scenario], rng: random.Random) -> Scenario:
    draw = rng.random()
    cumulative = 0.0
    for scenario in scenarios:
        cumulative += scenario.probability
        if draw <= cumulative:
            return scenario
    return scenarios[-1]


def choose_expected_value(strategies: list[Strategy], scenarios: list[Scenario]) -> Strategy:
    return max(strategies, key=lambda strategy: expected_value(strategy, scenarios))


def choose_ambiguity_averse(strategies: list[Strategy], scenarios: list[Scenario]) -> Strategy:
    return max(strategies, key=lambda strategy: ambiguity_adjusted_value(strategy, scenarios))


def choose_minimax_regret(strategies: list[Strategy], scenarios: list[Scenario]) -> Strategy:
    return min(strategies, key=lambda strategy: maximum_regret(strategy, strategies, scenarios))


def choose_adaptive(
    strategies: list[Strategy],
    scenario: Scenario,
    recent_loss_count: int,
    monitoring_trigger_active: bool,
) -> Strategy:
    if recent_loss_count >= 3 or monitoring_trigger_active:
        return max(
            strategies,
            key=lambda strategy: (
                strategy.reversibility,
                strategy.learning_capacity,
                strategy.robustness,
                strategy.implementation_capacity,
            ),
        )

    if scenario.model_shift >= 0.55:
        return max(
            strategies,
            key=lambda strategy: (
                -strategy.ambiguity_exposure,
                strategy.reversibility,
                strategy.learning_capacity,
            ),
        )

    return max(strategies, key=lambda strategy: expected_value(strategy, [scenario]))


def summarize_strategies(strategies: list[Strategy], scenarios: list[Scenario]) -> list[dict[str, object]]:
    regrets = regret_rows(strategies, scenarios)
    output: list[dict[str, object]] = []

    for strategy in strategies:
        values = [payoff(strategy, scenario) for scenario in scenarios]
        strategy_regrets = [float(row["regret"]) for row in regrets if row["strategy"] == strategy.name]

        output.append({
            "strategy": strategy.name,
            "expected_value": round(expected_value(strategy, scenarios), 4),
            "expected_utility": round(expected_utility(strategy, scenarios), 6),
            "ambiguity_adjusted_value": round(ambiguity_adjusted_value(strategy, scenarios), 6),
            "minimum_payoff": round(min(values), 4),
            "maximum_payoff": round(max(values), 4),
            "payoff_sd": round(pstdev(values), 4),
            "maximum_regret": round(max(strategy_regrets), 4),
            "average_regret": round(mean(strategy_regrets), 4),
            "robustness_share": round(robustness_share(strategy, scenarios), 4),
            "ambiguity_exposure": strategy.ambiguity_exposure,
            "reversibility": strategy.reversibility,
            "implementation_capacity": strategy.implementation_capacity,
            "evidence_quality": strategy.evidence_quality,
            "learning_capacity": strategy.learning_capacity,
        })

    return sorted(
        output,
        key=lambda row: (
            float(row["robustness_share"]),
            -float(row["maximum_regret"]),
            float(row["ambiguity_adjusted_value"]),
            float(row["expected_value"]),
        ),
        reverse=True,
    )


def simulate(
    strategies: list[Strategy],
    scenarios: list[Scenario],
    trials: int = 1000,
    seed: int = 42,
) -> list[dict[str, object]]:
    rng = random.Random(seed)
    expected_value_strategy = choose_expected_value(strategies, scenarios)
    ambiguity_strategy = choose_ambiguity_averse(strategies, scenarios)
    regret_strategy = choose_minimax_regret(strategies, scenarios)

    recent_loss_count = 0
    monitoring_trigger_active = False
    rows: list[dict[str, object]] = []

    for trial in range(1, trials + 1):
        scenario = weighted_choice(scenarios, rng)

        ev_payoff = payoff(expected_value_strategy, scenario)
        ambiguity_payoff = payoff(ambiguity_strategy, scenario)
        regret_payoff = payoff(regret_strategy, scenario)

        adaptive_strategy = choose_adaptive(
            strategies,
            scenario,
            recent_loss_count,
            monitoring_trigger_active,
        )
        adaptive_payoff = payoff(adaptive_strategy, scenario)

        if adaptive_payoff < 0:
            recent_loss_count += 1
        else:
            recent_loss_count = max(0, recent_loss_count - 1)

        monitoring_trigger_active = (
            recent_loss_count >= 2
            or scenario.model_shift >= 0.65
            or scenario.disruption >= 0.75
        )

        rows.append({
            "trial": trial,
            "scenario": scenario.name,
            "expected_value_strategy": expected_value_strategy.name,
            "expected_value_payoff": round(ev_payoff, 4),
            "ambiguity_averse_strategy": ambiguity_strategy.name,
            "ambiguity_averse_payoff": round(ambiguity_payoff, 4),
            "minimax_regret_strategy": regret_strategy.name,
            "minimax_regret_payoff": round(regret_payoff, 4),
            "adaptive_strategy": adaptive_strategy.name,
            "adaptive_payoff": round(adaptive_payoff, 4),
            "recent_loss_count": recent_loss_count,
            "monitoring_trigger_active": monitoring_trigger_active,
        })

    return rows


def summarize_simulation(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    agents = [
        ("Expected Value", "expected_value_payoff"),
        ("Ambiguity Averse", "ambiguity_averse_payoff"),
        ("Minimax Regret", "minimax_regret_payoff"),
        ("Adaptive", "adaptive_payoff"),
    ]

    output: list[dict[str, object]] = []

    for agent_name, field in agents:
        values = [float(row[field]) for row in rows]
        output.append({
            "agent": agent_name,
            "average_payoff": round(mean(values), 4),
            "minimum_payoff": round(min(values), 4),
            "maximum_payoff": round(max(values), 4),
            "payoff_sd": round(pstdev(values), 4),
            "loss_frequency": round(sum(1 for value in values if value < 0) / len(values), 4),
            "acceptable_frequency": round(sum(1 for value in values if value >= 40.0) / len(values), 4),
        })

    return sorted(output, key=lambda row: float(row["average_payoff"]), reverse=True)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"No rows to write: {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_decision_record(
    path: Path,
    strategy_summary: list[dict[str, object]],
    simulation_summary: list[dict[str, object]],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    record = {
        "article": "Why Uncertainty Changes Decision-Making",
        "decision_context": "Comparison of expected value, ambiguity aversion, minimax regret, and adaptive strategy under uncertain futures.",
        "robust_candidate": strategy_summary[0]["strategy"],
        "interpretive_warning": "The preferred strategy depends on uncertainty structure, ambiguity exposure, reversibility, downside risk, and the value of learning.",
        "modeling_principles": [
            "Distinguish risk from uncertainty, ambiguity, and deep uncertainty.",
            "Use expected value only when probabilities and outcomes are credible.",
            "Use ambiguity diagnostics when probability structure is poorly understood.",
            "Use regret and robustness when forecasts are fragile.",
            "Preserve reversibility when uncertainty is high and learning is possible.",
            "Document decision records for accountability and learning.",
            "Treat computational models as supports for judgment, not substitutes for responsibility.",
        ],
        "strategy_summary": strategy_summary,
        "simulation_summary": simulation_summary,
        "review_triggers": [
            "new evidence changes probability assumptions",
            "model shift indicator exceeds threshold",
            "loss frequency exceeds tolerance",
            "implementation capacity deteriorates",
            "scenario performance falls below acceptability threshold",
        ],
    }

    path.write_text(json.dumps(record, indent=2), encoding="utf-8")


def main() -> None:
    scenarios = load_scenarios()
    strategies = load_strategies()

    strategy_summary = summarize_strategies(strategies, scenarios)
    regret_output = regret_rows(strategies, scenarios)
    simulation_rows = simulate(strategies, scenarios, trials=1000, seed=42)
    simulation_summary = summarize_simulation(simulation_rows)

    write_csv(TABLES / "uncertainty_strategy_summary.csv", strategy_summary)
    write_csv(TABLES / "uncertainty_regret_table.csv", regret_output)
    write_csv(TABLES / "uncertainty_simulation_trials.csv", simulation_rows)
    write_csv(TABLES / "uncertainty_simulation_summary.csv", simulation_summary)
    write_decision_record(RECORDS / "uncertainty_decision_record.json", strategy_summary, simulation_summary)

    print("Uncertainty decision workflow complete.")
    print(TABLES / "uncertainty_strategy_summary.csv")
    print(TABLES / "uncertainty_simulation_summary.csv")
    print(RECORDS / "uncertainty_decision_record.json")


if __name__ == "__main__":
    main()
