#!/usr/bin/env python3
"""
Decision Science vs. Decision Theory Simulation

Compares:
- expected utility maximization
- minimax regret
- robust adaptive strategy
- satisficing under bounded rationality
- institutional stress testing
- decision-record export

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
    demand_multiplier: float
    cost_pressure: float
    disruption: float
    institutional_friction: float


@dataclass(frozen=True)
class Strategy:
    name: str
    upside_value: float
    base_cost: float
    resilience: float
    flexibility: float
    implementation_capacity: float
    evidence_quality: float
    legitimacy: float


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def load_scenarios() -> list[Scenario]:
    rows = read_csv_dicts(DATA / "synthetic_scenarios.csv")
    scenarios = [
        Scenario(
            row["scenario"],
            float(row["probability"]),
            float(row["demand_multiplier"]),
            float(row["cost_pressure"]),
            float(row["disruption"]),
            float(row["institutional_friction"]),
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
            float(row["upside_value"]),
            float(row["base_cost"]),
            float(row["resilience"]),
            float(row["flexibility"]),
            float(row["implementation_capacity"]),
            float(row["evidence_quality"]),
            float(row["legitimacy"]),
        )
        for row in rows
    ]


def validate_probabilities(scenarios: list[Scenario]) -> None:
    total = sum(s.probability for s in scenarios)
    if not math.isclose(total, 1.0, abs_tol=1e-9):
        raise ValueError(f"Scenario probabilities must sum to 1. Current sum: {total}")


def utility(value: float, risk_aversion: float = 0.018) -> float:
    return 1.0 - math.exp(-risk_aversion * value)


def payoff(strategy: Strategy, scenario: Scenario) -> float:
    gross_value = strategy.upside_value * scenario.demand_multiplier
    cost = strategy.base_cost * scenario.cost_pressure
    disruption_penalty = scenario.disruption * (1.0 - strategy.resilience) * 80.0
    friction_penalty = scenario.institutional_friction * (1.0 - strategy.implementation_capacity) * 60.0
    evidence_penalty = (1.0 - strategy.evidence_quality) * 18.0
    legitimacy_penalty = scenario.institutional_friction * (1.0 - strategy.legitimacy) * 35.0
    flexibility_credit = strategy.flexibility * scenario.disruption * 35.0

    return gross_value - cost - disruption_penalty - friction_penalty - evidence_penalty - legitimacy_penalty + flexibility_credit


def weighted_choice(scenarios: list[Scenario], rng: random.Random) -> Scenario:
    draw = rng.random()
    cumulative = 0.0
    for scenario in scenarios:
        cumulative += scenario.probability
        if draw <= cumulative:
            return scenario
    return scenarios[-1]


def expected_value(strategy: Strategy, scenarios: list[Scenario]) -> float:
    return sum(s.probability * payoff(strategy, s) for s in scenarios)


def expected_utility(strategy: Strategy, scenarios: list[Scenario]) -> float:
    return sum(s.probability * utility(payoff(strategy, s)) for s in scenarios)


def regret_table(strategies: list[Strategy], scenarios: list[Scenario]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for scenario in scenarios:
        scenario_payoffs = {strategy.name: payoff(strategy, scenario) for strategy in strategies}
        best_payoff = max(scenario_payoffs.values())
        for strategy in strategies:
            value = scenario_payoffs[strategy.name]
            rows.append({
                "scenario": scenario.name,
                "strategy": strategy.name,
                "payoff": round(value, 4),
                "best_payoff": round(best_payoff, 4),
                "regret": round(best_payoff - value, 4),
            })
    return rows


def maximum_regret(strategy: Strategy, strategies: list[Strategy], scenarios: list[Scenario]) -> float:
    rows = regret_table(strategies, scenarios)
    return max(float(row["regret"]) for row in rows if row["strategy"] == strategy.name)


def robustness_share(strategy: Strategy, scenarios: list[Scenario], threshold: float = 45.0) -> float:
    return sum(1 for scenario in scenarios if payoff(strategy, scenario) >= threshold) / len(scenarios)


def choose_expected_utility(strategies: list[Strategy], scenarios: list[Scenario]) -> Strategy:
    return max(strategies, key=lambda strategy: expected_utility(strategy, scenarios))


def choose_minimax_regret(strategies: list[Strategy], scenarios: list[Scenario]) -> Strategy:
    return min(strategies, key=lambda strategy: maximum_regret(strategy, strategies, scenarios))


def choose_robust_adaptive(strategies: list[Strategy], scenarios: list[Scenario]) -> Strategy:
    return max(
        strategies,
        key=lambda strategy: (
            robustness_share(strategy, scenarios),
            strategy.flexibility,
            strategy.resilience,
            strategy.legitimacy,
            expected_value(strategy, scenarios),
        ),
    )


def choose_satisficing(
    strategies: list[Strategy],
    scenario: Scenario,
    aspiration_threshold: float = 50.0,
) -> Strategy:
    search_order = sorted(
        strategies,
        key=lambda strategy: (
            -strategy.evidence_quality,
            -strategy.implementation_capacity,
            -strategy.legitimacy,
            strategy.base_cost,
        ),
    )

    for strategy in search_order:
        if payoff(strategy, scenario) >= aspiration_threshold:
            return strategy

    return search_order[-1]


def summarize_strategies(strategies: list[Strategy], scenarios: list[Scenario]) -> list[dict[str, object]]:
    regret_rows = regret_table(strategies, scenarios)
    output: list[dict[str, object]] = []

    for strategy in strategies:
        outcomes = [payoff(strategy, scenario) for scenario in scenarios]
        regrets = [float(row["regret"]) for row in regret_rows if row["strategy"] == strategy.name]
        output.append({
            "strategy": strategy.name,
            "expected_value": round(expected_value(strategy, scenarios), 4),
            "expected_utility": round(expected_utility(strategy, scenarios), 6),
            "minimum_payoff": round(min(outcomes), 4),
            "maximum_payoff": round(max(outcomes), 4),
            "payoff_sd": round(pstdev(outcomes), 4),
            "maximum_regret": round(max(regrets), 4),
            "average_regret": round(mean(regrets), 4),
            "robustness_share": round(robustness_share(strategy, scenarios), 4),
            "implementation_capacity": strategy.implementation_capacity,
            "evidence_quality": strategy.evidence_quality,
            "legitimacy": strategy.legitimacy,
        })

    return sorted(
        output,
        key=lambda row: (
            float(row["robustness_share"]),
            -float(row["maximum_regret"]),
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
    expected_utility_strategy = choose_expected_utility(strategies, scenarios)
    minimax_regret_strategy = choose_minimax_regret(strategies, scenarios)
    robust_adaptive_strategy = choose_robust_adaptive(strategies, scenarios)

    rows: list[dict[str, object]] = []

    for trial in range(1, trials + 1):
        scenario = weighted_choice(scenarios, rng)
        satisficing_strategy = choose_satisficing(strategies, scenario)

        rows.append({
            "trial": trial,
            "scenario": scenario.name,
            "expected_utility_strategy": expected_utility_strategy.name,
            "expected_utility_payoff": round(payoff(expected_utility_strategy, scenario), 4),
            "minimax_regret_strategy": minimax_regret_strategy.name,
            "minimax_regret_payoff": round(payoff(minimax_regret_strategy, scenario), 4),
            "robust_adaptive_strategy": robust_adaptive_strategy.name,
            "robust_adaptive_payoff": round(payoff(robust_adaptive_strategy, scenario), 4),
            "satisficing_strategy": satisficing_strategy.name,
            "satisficing_payoff": round(payoff(satisficing_strategy, scenario), 4),
        })

    return rows


def summarize_simulation(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    agents = [
        ("Expected Utility", "expected_utility_payoff"),
        ("Minimax Regret", "minimax_regret_payoff"),
        ("Robust Adaptive", "robust_adaptive_payoff"),
        ("Satisficing", "satisficing_payoff"),
    ]

    output: list[dict[str, object]] = []

    for agent_name, payoff_field in agents:
        values = [float(row[payoff_field]) for row in rows]
        output.append({
            "agent": agent_name,
            "average_payoff": round(mean(values), 4),
            "minimum_payoff": round(min(values), 4),
            "maximum_payoff": round(max(values), 4),
            "payoff_sd": round(pstdev(values), 4),
            "loss_frequency": round(sum(1 for value in values if value < 0) / len(values), 4),
            "acceptable_frequency": round(sum(1 for value in values if value >= 45.0) / len(values), 4),
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
        "article": "Decision Science vs. Decision Theory",
        "decision_context": "Comparison of formal decision-theoretic and applied decision-science criteria.",
        "selected_by_robust_diagnostic": strategy_summary[0]["strategy"],
        "interpretive_warning": "The preferred strategy depends on whether the decision-maker prioritizes expected utility, regret avoidance, robustness, or institutional feasibility.",
        "modeling_principles": [
            "Use expected utility when probabilities and utilities are defensible.",
            "Use regret and robustness when futures are uncertain or contested.",
            "Use satisficing models when bounded rationality and search constraints matter.",
            "Evaluate implementation capacity, evidence quality, and legitimacy alongside formal payoff.",
            "Treat computation as support for judgment, not a replacement for responsibility.",
        ],
        "strategy_summary": strategy_summary,
        "simulation_summary": simulation_summary,
    }
    path.write_text(json.dumps(record, indent=2), encoding="utf-8")


def main() -> None:
    scenarios = load_scenarios()
    strategies = load_strategies()

    strategy_summary = summarize_strategies(strategies, scenarios)
    regrets = regret_table(strategies, scenarios)
    simulation_rows = simulate(strategies, scenarios, trials=1000, seed=42)
    simulation_summary = summarize_simulation(simulation_rows)

    write_csv(TABLES / "strategy_summary.csv", strategy_summary)
    write_csv(TABLES / "regret_table.csv", regrets)
    write_csv(TABLES / "simulation_trials.csv", simulation_rows)
    write_csv(TABLES / "simulation_summary.csv", simulation_summary)
    write_decision_record(RECORDS / "decision_science_vs_decision_theory_record.json", strategy_summary, simulation_summary)

    print("Decision science vs. decision theory simulation complete.")
    print(TABLES / "strategy_summary.csv")
    print(TABLES / "simulation_summary.csv")
    print(RECORDS / "decision_science_vs_decision_theory_record.json")


if __name__ == "__main__":
    main()
