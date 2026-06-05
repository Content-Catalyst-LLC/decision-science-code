#!/usr/bin/env python3
"""
History of Decision Science Simulation

Compares historical decision paradigms:
- expected monetary value
- expected utility
- subjective expected utility
- satisficing
- noisy expected value
- minimax regret
- robustness

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
    subjective_probability: float


@dataclass(frozen=True)
class Strategy:
    name: str
    payoffs: tuple[float, ...]


def read_payoff_table() -> tuple[list[Scenario], list[Strategy]]:
    path = DATA / "synthetic_strategy_payoffs.csv"
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    scenarios = [
        Scenario(
            row["scenario"],
            float(row["objective_probability"]),
            float(row["subjective_probability"]),
        )
        for row in rows
    ]

    strategy_names = [name for name in rows[0] if name not in {"scenario", "objective_probability", "subjective_probability"}]
    strategies = [
        Strategy(name, tuple(float(row[name]) for row in rows))
        for name in strategy_names
    ]

    validate_probabilities([scenario.probability for scenario in scenarios], "Objective probabilities")
    validate_probabilities([scenario.subjective_probability for scenario in scenarios], "Subjective probabilities")

    return scenarios, strategies


def utility(value: float, risk_aversion: float = 0.016) -> float:
    return 1.0 - math.exp(-risk_aversion * value)


def validate_probabilities(values: list[float], label: str) -> None:
    total = sum(values)
    if not math.isclose(total, 1.0, abs_tol=1e-9):
        raise ValueError(f"{label} must sum to 1. Current sum: {total}")


def expected_value(strategy: Strategy, probabilities: list[float]) -> float:
    return sum(payoff * probability for payoff, probability in zip(strategy.payoffs, probabilities))


def expected_utility(strategy: Strategy, probabilities: list[float]) -> float:
    return sum(utility(payoff) * probability for payoff, probability in zip(strategy.payoffs, probabilities))


def regret_rows(strategies: list[Strategy], scenarios: list[Scenario]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for scenario_index, scenario in enumerate(scenarios):
        best_payoff = max(strategy.payoffs[scenario_index] for strategy in strategies)
        for strategy in strategies:
            payoff = strategy.payoffs[scenario_index]
            rows.append({
                "scenario": scenario.name,
                "strategy": strategy.name,
                "payoff": round(payoff, 4),
                "best_payoff": round(best_payoff, 4),
                "regret": round(best_payoff - payoff, 4),
            })
    return rows


def maximum_regret(strategy: Strategy, strategies: list[Strategy], scenarios: list[Scenario]) -> float:
    rows = regret_rows(strategies, scenarios)
    return max(float(row["regret"]) for row in rows if row["strategy"] == strategy.name)


def robustness_share(strategy: Strategy, threshold: float = 40.0) -> float:
    return sum(1 for payoff in strategy.payoffs if payoff >= threshold) / len(strategy.payoffs)


def weighted_scenario_index(scenarios: list[Scenario], rng: random.Random) -> int:
    draw = rng.random()
    cumulative = 0.0
    for index, scenario in enumerate(scenarios):
        cumulative += scenario.probability
        if draw <= cumulative:
            return index
    return len(scenarios) - 1


def choose_expected_value(strategies: list[Strategy], probabilities: list[float]) -> Strategy:
    return max(strategies, key=lambda strategy: expected_value(strategy, probabilities))


def choose_expected_utility(strategies: list[Strategy], probabilities: list[float]) -> Strategy:
    return max(strategies, key=lambda strategy: expected_utility(strategy, probabilities))


def choose_subjective_expected_utility(strategies: list[Strategy], subjective_probabilities: list[float]) -> Strategy:
    return max(strategies, key=lambda strategy: expected_utility(strategy, subjective_probabilities))


def choose_minimax_regret(strategies: list[Strategy], scenarios: list[Scenario]) -> Strategy:
    return min(strategies, key=lambda strategy: maximum_regret(strategy, strategies, scenarios))


def choose_satisficing(strategies: list[Strategy], scenario_index: int, threshold: float = 50.0) -> Strategy:
    search_order = ["Aggressive", "Balanced", "Adaptive", "Defensive"]
    lookup = {strategy.name: strategy for strategy in strategies}

    for name in search_order:
        candidate = lookup[name]
        if candidate.payoffs[scenario_index] >= threshold:
            return candidate

    return lookup[search_order[-1]]


def choose_noisy_expected_value(
    strategies: list[Strategy],
    probabilities: list[float],
    rng: random.Random,
    noise_scale: float = 8.0,
) -> Strategy:
    noisy_scores = {
        strategy.name: expected_value(strategy, probabilities) + rng.gauss(0.0, noise_scale)
        for strategy in strategies
    }
    selected_name = max(noisy_scores, key=noisy_scores.get)
    return next(strategy for strategy in strategies if strategy.name == selected_name)


def summarize_strategies(strategies: list[Strategy], scenarios: list[Scenario]) -> list[dict[str, object]]:
    probabilities = [scenario.probability for scenario in scenarios]
    subjective_probabilities = [scenario.subjective_probability for scenario in scenarios]
    regrets = regret_rows(strategies, scenarios)
    rows: list[dict[str, object]] = []

    for strategy in strategies:
        strategy_regrets = [float(row["regret"]) for row in regrets if row["strategy"] == strategy.name]
        rows.append({
            "strategy": strategy.name,
            "expected_value": round(expected_value(strategy, probabilities), 4),
            "expected_utility": round(expected_utility(strategy, probabilities), 6),
            "subjective_expected_utility": round(expected_utility(strategy, subjective_probabilities), 6),
            "minimum_payoff": round(min(strategy.payoffs), 4),
            "maximum_payoff": round(max(strategy.payoffs), 4),
            "payoff_sd": round(pstdev(strategy.payoffs), 4),
            "maximum_regret": round(max(strategy_regrets), 4),
            "average_regret": round(mean(strategy_regrets), 4),
            "robustness_share": round(robustness_share(strategy, threshold=40.0), 4),
            "satisficing_share": round(robustness_share(strategy, threshold=50.0), 4),
        })

    return sorted(
        rows,
        key=lambda row: (
            float(row["robustness_share"]),
            -float(row["maximum_regret"]),
            float(row["expected_value"]),
        ),
        reverse=True,
    )


def simulate(strategies: list[Strategy], scenarios: list[Scenario], trials: int = 1000, seed: int = 42) -> list[dict[str, object]]:
    rng = random.Random(seed)
    probabilities = [scenario.probability for scenario in scenarios]
    subjective_probabilities = [scenario.subjective_probability for scenario in scenarios]

    ev_strategy = choose_expected_value(strategies, probabilities)
    eu_strategy = choose_expected_utility(strategies, probabilities)
    seu_strategy = choose_subjective_expected_utility(strategies, subjective_probabilities)
    robust_strategy = choose_minimax_regret(strategies, scenarios)

    rows: list[dict[str, object]] = []

    for trial in range(1, trials + 1):
        scenario_index = weighted_scenario_index(scenarios, rng)
        scenario = scenarios[scenario_index]
        satisficing_strategy = choose_satisficing(strategies, scenario_index, threshold=50.0)
        noisy_strategy = choose_noisy_expected_value(strategies, probabilities, rng)

        rows.append({
            "trial": trial,
            "scenario": scenario.name,
            "expected_value_strategy": ev_strategy.name,
            "expected_value_payoff": round(ev_strategy.payoffs[scenario_index], 4),
            "expected_utility_strategy": eu_strategy.name,
            "expected_utility_payoff": round(eu_strategy.payoffs[scenario_index], 4),
            "subjective_expected_utility_strategy": seu_strategy.name,
            "subjective_expected_utility_payoff": round(seu_strategy.payoffs[scenario_index], 4),
            "robust_strategy": robust_strategy.name,
            "robust_payoff": round(robust_strategy.payoffs[scenario_index], 4),
            "satisficing_strategy": satisficing_strategy.name,
            "satisficing_payoff": round(satisficing_strategy.payoffs[scenario_index], 4),
            "noisy_expected_value_strategy": noisy_strategy.name,
            "noisy_expected_value_payoff": round(noisy_strategy.payoffs[scenario_index], 4),
        })

    return rows


def summarize_simulation(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    agents = [
        ("Expected Value", "expected_value_payoff"),
        ("Expected Utility", "expected_utility_payoff"),
        ("Subjective Expected Utility", "subjective_expected_utility_payoff"),
        ("Robust Minimax Regret", "robust_payoff"),
        ("Satisficing", "satisficing_payoff"),
        ("Noisy Expected Value", "noisy_expected_value_payoff"),
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


def write_decision_record(path: Path, strategy_summary: list[dict[str, object]], simulation_summary: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "article": "The History of Decision Science",
        "decision_context": "Comparison of historical decision paradigms under uncertainty.",
        "historical_interpretation": "Different eras of decision science emphasize different criteria: expectation, utility, subjective belief, bounded rationality, regret, and robustness.",
        "robust_candidate": strategy_summary[0]["strategy"],
        "strategy_summary": strategy_summary,
        "simulation_summary": simulation_summary,
        "modeling_principles": [
            "Expected value represents early probability-weighted payoff reasoning.",
            "Expected utility represents subjective valuation and risk attitude.",
            "Subjective expected utility represents coherent belief under uncertainty.",
            "Satisficing represents bounded rationality and limited search.",
            "Minimax regret represents robust decision-making under uncertain futures.",
            "Noisy expected value represents judgment under imperfect attention and estimation noise.",
            "Computational models support historical interpretation but do not replace judgment.",
        ],
    }
    path.write_text(json.dumps(record, indent=2), encoding="utf-8")


def main() -> None:
    scenarios, strategies = read_payoff_table()
    strategy_summary = summarize_strategies(strategies, scenarios)
    regrets = regret_rows(strategies, scenarios)
    simulation_rows = simulate(strategies, scenarios, trials=1000, seed=42)
    simulation_summary = summarize_simulation(simulation_rows)

    write_csv(TABLES / "historical_strategy_summary.csv", strategy_summary)
    write_csv(TABLES / "historical_regret_table.csv", regrets)
    write_csv(TABLES / "historical_simulation_trials.csv", simulation_rows)
    write_csv(TABLES / "historical_simulation_summary.csv", simulation_summary)
    write_decision_record(RECORDS / "history_of_decision_science_record.json", strategy_summary, simulation_summary)

    print("History of decision science workflow complete.")
    print(TABLES / "historical_strategy_summary.csv")
    print(TABLES / "historical_simulation_summary.csv")
    print(RECORDS / "history_of_decision_science_record.json")


if __name__ == "__main__":
    main()
