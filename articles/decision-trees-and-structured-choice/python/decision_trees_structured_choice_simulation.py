#!/usr/bin/env python3
"""
Decision Trees and Structured Choice Simulation

Computes expected value, robust score, simulation outcomes, regret,
thresholds, value of information, and decision records.

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
    success_payoff: float
    failure_payoff: float
    success_probability: float
    information_cost: float
    flexibility_credit: float
    description: str


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def load_strategies() -> list[Strategy]:
    rows = read_csv_dicts(DATA / "synthetic_tree_strategies.csv")
    return [
        Strategy(
            row["strategy"],
            float(row["success_payoff"]),
            float(row["failure_payoff"]),
            float(row["success_probability"]),
            float(row["information_cost"]),
            float(row["flexibility_credit"]),
            row["description"],
        )
        for row in rows
    ]


def expected_value(strategy: Strategy, success_probability: float | None = None) -> float:
    p = strategy.success_probability if success_probability is None else success_probability
    return (
        strategy.success_payoff * p
        + strategy.failure_payoff * (1.0 - p)
        - strategy.information_cost
        + strategy.flexibility_credit
    )


def robust_score(strategy: Strategy) -> float:
    minimum_outcome = min(strategy.success_payoff, strategy.failure_payoff)
    maximum_outcome = max(strategy.success_payoff, strategy.failure_payoff)
    outcome_spread = maximum_outcome - minimum_outcome
    return 0.60 * expected_value(strategy) + 0.25 * minimum_outcome - 0.15 * outcome_spread


def rollback_profiles(strategies: list[Strategy]) -> list[dict[str, object]]:
    rows = []
    for strategy in strategies:
        minimum_outcome = min(strategy.success_payoff, strategy.failure_payoff)
        maximum_outcome = max(strategy.success_payoff, strategy.failure_payoff)
        outcome_spread = maximum_outcome - minimum_outcome
        rows.append({
            "strategy": strategy.name,
            "description": strategy.description,
            "success_payoff": strategy.success_payoff,
            "failure_payoff": strategy.failure_payoff,
            "success_probability": strategy.success_probability,
            "failure_probability": round(1.0 - strategy.success_probability, 4),
            "information_cost": strategy.information_cost,
            "flexibility_credit": strategy.flexibility_credit,
            "expected_value": round(expected_value(strategy), 4),
            "minimum_outcome": minimum_outcome,
            "maximum_outcome": maximum_outcome,
            "outcome_spread": outcome_spread,
            "robust_score": round(robust_score(strategy), 4),
        })

    by_ev = sorted(rows, key=lambda row: float(row["expected_value"]), reverse=True)
    by_robust = sorted(rows, key=lambda row: float(row["robust_score"]), reverse=True)

    for rank, row in enumerate(by_ev, start=1):
        row["expected_value_rank"] = rank

    for rank, row in enumerate(by_robust, start=1):
        row["robust_rank"] = rank

    return sorted(rows, key=lambda row: float(row["expected_value"]), reverse=True)


def simulate_strategy(strategy: Strategy, trials: int, seed: int) -> list[dict[str, object]]:
    rng = random.Random(seed)
    rows: list[dict[str, object]] = []

    for trial in range(1, trials + 1):
        success = rng.random() < strategy.success_probability
        payoff = strategy.success_payoff if success else strategy.failure_payoff
        realized_value = payoff - strategy.information_cost + strategy.flexibility_credit

        review_trigger = (
            realized_value < 0
            or (not success and strategy.success_probability >= 0.55)
            or strategy.failure_payoff < -25
        )

        rows.append({
            "trial": trial,
            "strategy": strategy.name,
            "success": success,
            "realized_value": round(realized_value, 4),
            "review_trigger": review_trigger,
        })

    return rows


def regret_rows(trial_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[int, list[dict[str, object]]] = {}

    for row in trial_rows:
        grouped.setdefault(int(row["trial"]), []).append(row)

    output: list[dict[str, object]] = []

    for trial, rows in grouped.items():
        best_value = max(float(row["realized_value"]) for row in rows)
        for row in rows:
            realized = float(row["realized_value"])
            output.append({
                "trial": trial,
                "strategy": row["strategy"],
                "realized_value": realized,
                "best_trial_value": best_value,
                "regret": round(best_value - realized, 4),
                "review_trigger": row["review_trigger"],
            })

    return output


def summarize_simulation(rows: list[dict[str, object]], strategies: list[Strategy]) -> list[dict[str, object]]:
    output: list[dict[str, object]] = []

    for strategy in strategies:
        strategy_rows = [row for row in rows if row["strategy"] == strategy.name]
        values = [float(row["realized_value"]) for row in strategy_rows]
        regrets = [float(row["regret"]) for row in strategy_rows]
        triggers = [bool(row["review_trigger"]) for row in strategy_rows]

        output.append({
            "strategy": strategy.name,
            "expected_value": round(expected_value(strategy), 4),
            "robust_score": round(robust_score(strategy), 4),
            "average_realized_value": round(mean(values), 4),
            "minimum_realized_value": round(min(values), 4),
            "maximum_realized_value": round(max(values), 4),
            "value_sd": round(pstdev(values), 4),
            "average_regret": round(mean(regrets), 4),
            "maximum_regret": round(max(regrets), 4),
            "review_trigger_rate": round(sum(1 for trigger in triggers if trigger) / len(triggers), 4),
        })

    return sorted(output, key=lambda row: float(row["expected_value"]), reverse=True)


def threshold_analysis(strategy: Strategy, baseline_value: float) -> dict[str, object]:
    threshold = None

    for i in range(0, 101):
        probability = i / 100
        value = expected_value(strategy, success_probability=probability)
        if value >= baseline_value:
            threshold = probability
            break

    return {
        "strategy": strategy.name,
        "threshold_to_exceed_baseline": threshold,
        "baseline_expected_value": round(baseline_value, 4),
    }


def probability_sensitivity(strategies: list[Strategy]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    for strategy in strategies:
        for i in range(30, 86):
            probability = i / 100
            rows.append({
                "strategy": strategy.name,
                "success_probability": probability,
                "expected_value": round(expected_value(strategy, probability), 4),
            })

    return rows


def value_of_information(strategies: list[Strategy]) -> dict[str, object]:
    immediate = next(strategy for strategy in strategies if strategy.name == "Immediate Action")
    staged = next(strategy for strategy in strategies if strategy.name == "Staged Learning")
    return {
        "comparison": "Staged Learning vs Immediate Action",
        "immediate_expected_value": round(expected_value(immediate), 4),
        "staged_expected_value": round(expected_value(staged), 4),
        "net_value_of_information": round(expected_value(staged) - expected_value(immediate), 4),
    }


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
    strategies = load_strategies()

    profiles = rollback_profiles(strategies)
    sensitivity = probability_sensitivity(strategies)
    voi = value_of_information(strategies)

    all_trial_rows: list[dict[str, object]] = []
    for index, strategy in enumerate(strategies):
        all_trial_rows.extend(simulate_strategy(strategy, trials=1000, seed=42 + index))

    regret_detail = regret_rows(all_trial_rows)
    simulation_summary = summarize_simulation(regret_detail, strategies)

    baseline = next(strategy for strategy in strategies if strategy.name == "Conservative Baseline")
    baseline_value = expected_value(baseline)
    thresholds = [threshold_analysis(strategy, baseline_value) for strategy in strategies]

    write_csv(TABLES / "decision_tree_rollback_profiles.csv", profiles)
    write_csv(TABLES / "decision_tree_probability_sensitivity.csv", sensitivity)
    write_csv(TABLES / "value_of_information_summary.csv", [voi])
    write_csv(TABLES / "decision_tree_simulation_trials.csv", regret_detail)
    write_csv(TABLES / "decision_tree_strategy_summary.csv", simulation_summary)
    write_csv(TABLES / "decision_tree_threshold_analysis.csv", thresholds)

    write_json(
        RECORDS / "decision_tree_structured_choice_record.json",
        {
            "article": "Decision Trees and Structured Choice",
            "decision_context": "Sequential decision-tree comparison with expected value, regret, and review triggers.",
            "modeling_principles": [
                "Represent decisions, uncertainties, and outcomes explicitly.",
                "Roll back chance nodes using expected value or utility.",
                "Compare decision nodes by downstream value.",
                "Test threshold sensitivity.",
                "Track regret and downside exposure.",
                "Use review triggers when realized outcomes contradict assumptions.",
                "Treat the tree as decision support, not a substitute for judgment.",
            ],
            "rollback_profiles": profiles,
            "simulation_summary": simulation_summary,
            "thresholds": thresholds,
            "value_of_information": voi,
        },
    )

    print("Decision-tree structured choice workflow complete.")
    print(TABLES / "decision_tree_rollback_profiles.csv")
    print(TABLES / "decision_tree_strategy_summary.csv")
    print(TABLES / "decision_tree_threshold_analysis.csv")
    print(RECORDS / "decision_tree_structured_choice_record.json")


if __name__ == "__main__":
    main()
