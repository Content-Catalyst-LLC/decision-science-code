#!/usr/bin/env python3
"""
Sensitivity Analysis and Scenario Comparison Simulation

Computes scenario performance, robustness scores, regret,
downside breach rates, one-way sensitivity, threshold analysis,
probabilistic sensitivity, key-driver diagnostics, and a decision record.

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

QUALITY_SCORES = {"high": 1.0, "medium": 0.65, "low": 0.35}


@dataclass(frozen=True)
class Strategy:
    name: str
    base_value: float
    demand_sensitivity: float
    cost_sensitivity: float
    disruption_sensitivity: float
    resilience_buffer: float
    adaptation_capacity: float
    cost_score: float
    resilience_score: float
    flexibility_score: float
    implementation_score: float
    downside_protection: float
    description: str


@dataclass(frozen=True)
class Scenario:
    name: str
    demand_shift: float
    cost_pressure: float
    disruption_pressure: float
    volatility: float
    probability: float
    description: str


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def load_strategies() -> list[Strategy]:
    rows = read_csv_dicts(DATA / "synthetic_strategies.csv")
    return [
        Strategy(
            row["strategy"],
            float(row["base_value"]),
            float(row["demand_sensitivity"]),
            float(row["cost_sensitivity"]),
            float(row["disruption_sensitivity"]),
            float(row["resilience_buffer"]),
            float(row["adaptation_capacity"]),
            float(row["cost_score"]),
            float(row["resilience_score"]),
            float(row["flexibility_score"]),
            float(row["implementation_score"]),
            float(row["downside_protection"]),
            row["description"],
        )
        for row in rows
    ]


def load_scenarios() -> list[Scenario]:
    rows = read_csv_dicts(DATA / "synthetic_scenarios.csv")
    return [
        Scenario(
            row["scenario"],
            float(row["demand_shift"]),
            float(row["cost_pressure"]),
            float(row["disruption_pressure"]),
            float(row["volatility"]),
            float(row["probability"]),
            row["description"],
        )
        for row in rows
    ]


def evaluate_strategy(strategy: Strategy, scenario: Scenario, rng: random.Random | None = None) -> float:
    random_shock = 0.0 if rng is None else rng.gauss(0.0, scenario.volatility)

    value = (
        strategy.base_value
        + strategy.demand_sensitivity * scenario.demand_shift
        - strategy.cost_sensitivity * scenario.cost_pressure
        - strategy.disruption_sensitivity * scenario.disruption_pressure
        + strategy.resilience_buffer * max(0.0, scenario.disruption_pressure)
        + strategy.adaptation_capacity * abs(scenario.demand_shift)
        + random_shock
    )

    return value


def simulate(
    strategies: list[Strategy],
    scenarios: list[Scenario],
    trials_per_scenario: int = 750,
    seed: int = 42,
) -> list[dict[str, object]]:
    rng = random.Random(seed)
    rows: list[dict[str, object]] = []

    for scenario in scenarios:
        for trial in range(1, trials_per_scenario + 1):
            scenario_values = {
                strategy.name: evaluate_strategy(strategy, scenario, rng)
                for strategy in strategies
            }
            best_value = max(scenario_values.values())

            for strategy_name, value in scenario_values.items():
                rows.append({
                    "scenario": scenario.name,
                    "trial": trial,
                    "strategy": strategy_name,
                    "value": round(value, 6),
                    "best_trial_value": round(best_value, 6),
                    "regret": round(best_value - value, 6),
                    "downside_breach": value < 55.0,
                    "scenario_probability": scenario.probability,
                })

    return rows


def summarize(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    strategies = sorted({str(row["strategy"]) for row in rows})
    output: list[dict[str, object]] = []

    for strategy in strategies:
        subset = [row for row in rows if row["strategy"] == strategy]
        values = [float(row["value"]) for row in subset]
        regrets = [float(row["regret"]) for row in subset]
        breaches = [bool(row["downside_breach"]) for row in subset]

        scenario_averages: list[float] = []
        scenario_minima: list[float] = []

        for scenario in sorted({str(row["scenario"]) for row in subset}):
            scenario_rows = [row for row in subset if row["scenario"] == scenario]
            scenario_values = [float(row["value"]) for row in scenario_rows]
            scenario_averages.append(mean(scenario_values))
            scenario_minima.append(min(scenario_values))

        average_value = mean(values)
        minimum_scenario_average = min(scenario_averages)
        worst_observed_value = min(values)
        average_regret = mean(regrets)
        maximum_regret = max(regrets)
        downside_breach_rate = sum(1 for breach in breaches if breach) / len(breaches)
        volatility = pstdev(values)

        robustness_score = (
            0.35 * average_value
            + 0.30 * minimum_scenario_average
            + 0.20 * worst_observed_value
            - 0.10 * maximum_regret
            - 0.05 * volatility
        )

        output.append({
            "strategy": strategy,
            "average_value": round(average_value, 6),
            "minimum_scenario_average": round(minimum_scenario_average, 6),
            "worst_observed_value": round(worst_observed_value, 6),
            "volatility": round(volatility, 6),
            "average_regret": round(average_regret, 6),
            "maximum_regret": round(maximum_regret, 6),
            "downside_breach_rate": round(downside_breach_rate, 6),
            "robustness_score": round(robustness_score, 6),
        })

    return sorted(output, key=lambda row: float(row["robustness_score"]), reverse=True)


def scenario_summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    output: list[dict[str, object]] = []
    scenarios = sorted({str(row["scenario"]) for row in rows})
    strategies = sorted({str(row["strategy"]) for row in rows})

    for scenario in scenarios:
        for strategy in strategies:
            subset = [
                row for row in rows
                if row["scenario"] == scenario and row["strategy"] == strategy
            ]
            values = [float(row["value"]) for row in subset]
            regrets = [float(row["regret"]) for row in subset]
            output.append({
                "scenario": scenario,
                "strategy": strategy,
                "average_value": round(mean(values), 6),
                "minimum_value": round(min(values), 6),
                "average_regret": round(mean(regrets), 6),
                "maximum_regret": round(max(regrets), 6),
                "downside_breach_rate": round(
                    sum(1 for row in subset if bool(row["downside_breach"])) / len(subset),
                    6,
                ),
            })

    return output


def threshold_analysis(strategies: list[Strategy]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    demand_values = [x / 10 for x in range(-20, 31)]

    for demand_shift in demand_values:
        scenario = Scenario("Threshold Test", demand_shift, 0.50, 0.50, 0.0, 1.0, "Demand threshold scan")
        scores = {
            strategy.name: evaluate_strategy(strategy, scenario, None)
            for strategy in strategies
        }
        winner = max(scores.items(), key=lambda item: item[1])

        rows.append({
            "demand_shift": demand_shift,
            "winning_strategy": winner[0],
            "winning_value": round(winner[1], 6),
        })

    return rows


def one_way_sensitivity(strategies: list[Strategy]) -> list[dict[str, object]]:
    parameters = read_csv_dicts(DATA / "synthetic_parameters.csv")
    rows: list[dict[str, object]] = []

    baseline = Scenario("Baseline Sensitivity", 0.50, 0.30, 0.20, 0.0, 1.0, "Baseline one-way sensitivity")

    for parameter in parameters:
        name = parameter["parameter"]
        if name not in {"demand_shift", "cost_pressure", "disruption_pressure"}:
            continue

        for value in [float(parameter["low"]), float(parameter["baseline"]), float(parameter["high"])]:
            scenario = Scenario(
                "One-Way Sensitivity",
                value if name == "demand_shift" else baseline.demand_shift,
                value if name == "cost_pressure" else baseline.cost_pressure,
                value if name == "disruption_pressure" else baseline.disruption_pressure,
                0.0,
                1.0,
                "One-way parameter variation",
            )

            scores = {
                strategy.name: evaluate_strategy(strategy, scenario, None)
                for strategy in strategies
            }
            winner = max(scores.items(), key=lambda item: item[1])

            for strategy_name, score in scores.items():
                rows.append({
                    "parameter": name,
                    "parameter_value": value,
                    "strategy": strategy_name,
                    "score": round(score, 6),
                    "winning_strategy": winner[0],
                })

    return rows


def probabilistic_sensitivity(strategies: list[Strategy], trials: int = 3000, seed: int = 123) -> list[dict[str, object]]:
    rng = random.Random(seed)
    rows: list[dict[str, object]] = []

    for trial in range(1, trials + 1):
        scenario = Scenario(
            "Probabilistic Sensitivity",
            rng.uniform(-1.5, 2.5),
            rng.uniform(0.0, 1.4),
            rng.uniform(0.0, 1.7),
            rng.uniform(1.0, 7.0),
            1.0,
            "Randomized uncertainty draw",
        )

        values = {strategy.name: evaluate_strategy(strategy, scenario, rng) for strategy in strategies}
        best_value = max(values.values())

        for strategy_name, value in values.items():
            rows.append({
                "trial": trial,
                "strategy": strategy_name,
                "value": round(value, 6),
                "regret": round(best_value - value, 6),
                "winner": strategy_name == max(values.items(), key=lambda item: item[1])[0],
                "downside_breach": value < 55.0,
            })

    return rows


def probabilistic_summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    output: list[dict[str, object]] = []

    for strategy in sorted({str(row["strategy"]) for row in rows}):
        subset = [row for row in rows if row["strategy"] == strategy]
        values = [float(row["value"]) for row in subset]
        regrets = [float(row["regret"]) for row in subset]
        output.append({
            "strategy": strategy,
            "average_value": round(mean(values), 6),
            "minimum_value": round(min(values), 6),
            "maximum_value": round(max(values), 6),
            "value_volatility": round(pstdev(values), 6),
            "average_regret": round(mean(regrets), 6),
            "maximum_regret": round(max(regrets), 6),
            "win_rate": round(sum(1 for row in subset if bool(row["winner"])) / len(subset), 6),
            "downside_breach_rate": round(sum(1 for row in subset if bool(row["downside_breach"])) / len(subset), 6),
        })

    return sorted(output, key=lambda row: float(row["win_rate"]), reverse=True)


def key_driver_diagnostics(one_way_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    output: list[dict[str, object]] = []

    for parameter in sorted({str(row["parameter"]) for row in one_way_rows}):
        subset = [row for row in one_way_rows if row["parameter"] == parameter]
        parameter_scores = [float(row["score"]) for row in subset]
        winners = sorted({str(row["winning_strategy"]) for row in subset})
        output.append({
            "parameter": parameter,
            "score_range": round(max(parameter_scores) - min(parameter_scores), 6),
            "winner_count": len(winners),
            "winning_strategies_observed": "; ".join(winners),
            "driver_flag": "high" if len(winners) > 1 else "stable",
        })

    return sorted(output, key=lambda row: float(row["score_range"]), reverse=True)


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
    scenarios = load_scenarios()

    trial_rows = simulate(strategies, scenarios, trials_per_scenario=750, seed=42)
    robustness_rows = summarize(trial_rows)
    scenario_rows = scenario_summary(trial_rows)
    threshold_rows = threshold_analysis(strategies)
    one_way_rows = one_way_sensitivity(strategies)
    driver_rows = key_driver_diagnostics(one_way_rows)
    probabilistic_rows = probabilistic_sensitivity(strategies, trials=3000, seed=123)
    probabilistic_summary_rows = probabilistic_summary(probabilistic_rows)

    write_csv(TABLES / "scenario_simulation_trials.csv", trial_rows)
    write_csv(TABLES / "strategy_robustness_summary.csv", robustness_rows)
    write_csv(TABLES / "scenario_strategy_summary.csv", scenario_rows)
    write_csv(TABLES / "demand_threshold_analysis.csv", threshold_rows)
    write_csv(TABLES / "one_way_sensitivity_results.csv", one_way_rows)
    write_csv(TABLES / "key_driver_diagnostics.csv", driver_rows)
    write_csv(TABLES / "probabilistic_sensitivity_trials.csv", probabilistic_rows)
    write_csv(TABLES / "probabilistic_sensitivity_summary.csv", probabilistic_summary_rows)

    write_json(
        RECORDS / "sensitivity_scenario_decision_record.json",
        {
            "article": "Sensitivity Analysis and Scenario Comparison",
            "decision_context": "Testing strategy performance across uncertain scenarios, parameters, regret, and robustness conditions.",
            "modeling_principles": [
                "Baseline results should not be treated as final recommendations.",
                "Decision rankings should be tested under plausible parameter variation.",
                "Scenarios should represent coherent alternative futures.",
                "Robustness requires acceptable performance across multiple conditions.",
                "Regret reveals the cost of being wrong in particular scenarios.",
                "Threshold analysis identifies when decisions should be reviewed.",
                "Sensitivity results should be preserved in accountable decision records.",
            ],
            "robustness_summary": robustness_rows,
            "key_driver_diagnostics": driver_rows,
            "probabilistic_sensitivity_summary": probabilistic_summary_rows,
            "threshold_summary": threshold_rows,
        },
    )

    print("Sensitivity analysis and scenario comparison workflow complete.")
    print(TABLES / "strategy_robustness_summary.csv")
    print(TABLES / "scenario_strategy_summary.csv")
    print(TABLES / "demand_threshold_analysis.csv")
    print(TABLES / "key_driver_diagnostics.csv")
    print(TABLES / "probabilistic_sensitivity_summary.csv")
    print(RECORDS / "sensitivity_scenario_decision_record.json")


if __name__ == "__main__":
    main()
