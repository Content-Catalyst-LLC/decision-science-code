#!/usr/bin/env python3
"""
Decision-Making Under Deep Uncertainty workflow.

Simulates strategy performance across ambiguous futures, ambiguity profiles,
regret, robustness, threshold compliance, vulnerability conditions, adaptive
strategy performance, and decision-record export.

Uses only the Python standard library.
"""

from __future__ import annotations

from pathlib import Path
import csv
import json
import random
from statistics import mean, stdev

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
DATA = ARTICLE_ROOT / "data"
TABLES = ARTICLE_ROOT / "outputs" / "tables"
RECORDS = ARTICLE_ROOT / "outputs" / "decision_records"


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def load_scenarios() -> list[str]:
    return [row["scenario"] for row in read_csv_dicts(DATA / "synthetic_scenarios.csv")]


def load_performance_matrix() -> list[dict[str, object]]:
    scenarios = load_scenarios()
    rows = read_csv_dicts(DATA / "synthetic_performance_matrix.csv")
    output: list[dict[str, object]] = []
    for row in rows:
        item: dict[str, object] = {"strategy": row["strategy"]}
        for scenario in scenarios:
            item[scenario] = float(row[scenario])
        output.append(item)
    return output


def load_strategy_parameters() -> dict[str, dict[str, float]]:
    output: dict[str, dict[str, float]] = {}
    for row in read_csv_dicts(DATA / "synthetic_strategies.csv"):
        output[row["strategy"]] = {
            "base_return": float(row["base_return"]),
            "volatility": float(row["volatility"]),
            "adaptability": float(row["adaptability"]),
            "resilience": float(row["resilience"]),
        }
    return output


def load_thresholds() -> dict[str, float]:
    return {
        row["threshold_name"]: float(row["value"])
        for row in read_csv_dicts(DATA / "synthetic_thresholds.csv")
    }


def load_ambiguity_profiles() -> dict[str, dict[str, float]]:
    rows = read_csv_dicts(DATA / "synthetic_ambiguity_profiles.csv")
    profiles = sorted({row["profile"] for row in rows})
    output: dict[str, dict[str, float]] = {}
    for profile in profiles:
        weights = {
            row["scenario"]: float(row["weight"])
            for row in rows
            if row["profile"] == profile
        }
        ensure_weights(weights)
        output[profile] = weights
    return output


def ensure_weights(weights: dict[str, float]) -> None:
    scenarios = load_scenarios()
    total = sum(weights.values())
    if abs(total - 1.0) > 1e-6:
        raise ValueError(f"Weights must sum to 1. Got {total}.")
    for scenario in scenarios:
        if scenario not in weights:
            raise ValueError(f"Missing scenario weight: {scenario}")


def rank_rows(rows: list[dict[str, object]], score_field: str) -> list[dict[str, object]]:
    output: list[dict[str, object]] = []
    for rank, row in enumerate(sorted(rows, key=lambda x: float(x[score_field]), reverse=True), start=1):
        item = dict(row)
        item["rank"] = rank
        output.append(item)
    return output


def compute_regret_matrix(performance_rows: list[dict[str, object]], scenarios: list[str]) -> list[dict[str, object]]:
    scenario_maxima = {
        scenario: max(float(row[scenario]) for row in performance_rows)
        for scenario in scenarios
    }

    rows: list[dict[str, object]] = []
    for strategy in performance_rows:
        item: dict[str, object] = {"strategy": strategy["strategy"]}
        for scenario in scenarios:
            item[scenario] = round(scenario_maxima[scenario] - float(strategy[scenario]), 6)
        rows.append(item)

    return rows


def compute_vulnerability_table(
    performance_rows: list[dict[str, object]],
    scenarios: list[str],
    threshold: float,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for strategy in performance_rows:
        item: dict[str, object] = {"strategy": strategy["strategy"]}
        for scenario in scenarios:
            item[scenario] = float(strategy[scenario]) < threshold
        rows.append(item)
    return rows


def compute_robustness_results() -> list[dict[str, object]]:
    scenarios = load_scenarios()
    performance_rows = load_performance_matrix()
    profiles = load_ambiguity_profiles()
    thresholds = load_thresholds()

    performance_threshold = thresholds["minimum_acceptable_performance"]
    high_regret_threshold = thresholds["high_regret_threshold"]
    low_worst_case_threshold = thresholds["low_worst_case_threshold"]
    low_pass_rate_threshold = thresholds["low_pass_rate_threshold"]

    scenario_maxima = {
        scenario: max(float(strategy[scenario]) for strategy in performance_rows)
        for scenario in scenarios
    }

    all_rows: list[dict[str, object]] = []

    for profile_name, weights in profiles.items():
        profile_rows: list[dict[str, object]] = []

        for strategy in performance_rows:
            performances = [float(strategy[scenario]) for scenario in scenarios]
            regrets = [
                scenario_maxima[scenario] - float(strategy[scenario])
                for scenario in scenarios
            ]

            expected_value = sum(float(strategy[scenario]) * weights[scenario] for scenario in scenarios)
            worst_case = min(performances)
            best_case = max(performances)
            performance_range = best_case - worst_case
            average_regret = mean(regrets)
            max_regret = max(regrets)
            threshold_pass_rate = sum(1 for value in performances if value >= performance_threshold) / len(performances)
            vulnerability_count = sum(1 for value in performances if value < performance_threshold)

            robustness_score = (
                0.28 * worst_case
                + 0.24 * threshold_pass_rate
                + 0.20 * (1 - max_regret)
                + 0.18 * expected_value
                + 0.10 * (1 - performance_range)
            )

            review = (
                worst_case < low_worst_case_threshold
                or max_regret > high_regret_threshold
                or threshold_pass_rate < low_pass_rate_threshold
            )

            profile_rows.append({
                "profile": profile_name,
                "strategy": strategy["strategy"],
                "expected_value": round(expected_value, 6),
                "worst_case": round(worst_case, 6),
                "best_case": round(best_case, 6),
                "performance_range": round(performance_range, 6),
                "average_regret": round(average_regret, 6),
                "max_regret": round(max_regret, 6),
                "threshold_pass_rate": round(threshold_pass_rate, 6),
                "vulnerability_count": vulnerability_count,
                "robustness_score": round(robustness_score, 6),
                "review_flag": "review" if review else "acceptable",
            })

        all_rows.extend(rank_rows(profile_rows, "robustness_score"))

    return all_rows


def scenario_summary(performance_rows: list[dict[str, object]], scenarios: list[str]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for scenario in scenarios:
        values = [(strategy["strategy"], float(strategy[scenario])) for strategy in performance_rows]
        best_strategy, max_performance = max(values, key=lambda item: item[1])
        _, min_performance = min(values, key=lambda item: item[1])

        rows.append({
            "scenario": scenario,
            "best_strategy": best_strategy,
            "max_performance": round(max_performance, 6),
            "min_performance": round(min_performance, 6),
            "scenario_spread": round(max_performance - min_performance, 6),
        })

    return rows


def simulate_strategy(strategy_name: str, params: dict[str, float], time_steps: int, rng: random.Random) -> list[dict[str, object]]:
    value = 100.0
    rows: list[dict[str, object]] = []

    for time in range(1, time_steps + 1):
        regime_shift = rng.choices(
            population=[-2.5, -1.0, 0.0, 1.0, 2.0],
            weights=[0.10, 0.20, 0.30, 0.25, 0.15],
            k=1,
        )[0]

        structural_shock = rng.gauss(0.0, params["volatility"])
        adaptive_buffer = params["adaptability"] * rng.uniform(0.4, 1.4)
        resilience_buffer = params["resilience"] * rng.uniform(0.3, 1.0)

        growth = params["base_return"] + regime_shift + structural_shock + adaptive_buffer + resilience_buffer
        value = max(20.0, value * (1.0 + growth / 100.0))

        rows.append({
            "strategy": strategy_name,
            "time": time,
            "strategy_value_index": round(value, 6),
            "growth_rate": round(growth, 6),
            "regime_shift": round(regime_shift, 6),
            "structural_shock": round(structural_shock, 6),
        })

    return rows


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
    scenarios = load_scenarios()
    performance_rows = load_performance_matrix()
    thresholds = load_thresholds()
    profiles = load_ambiguity_profiles()
    strategy_parameters = load_strategy_parameters()

    robustness = compute_robustness_results()
    regrets = compute_regret_matrix(performance_rows, scenarios)
    vulnerabilities = compute_vulnerability_table(
        performance_rows,
        scenarios,
        thresholds["minimum_acceptable_performance"],
    )
    scenario_rows = scenario_summary(performance_rows, scenarios)

    rng = random.Random(42)
    simulation_rows: list[dict[str, object]] = []

    for strategy_name, params in strategy_parameters.items():
        simulation_rows.extend(simulate_strategy(strategy_name, params, time_steps=40, rng=rng))

    simulation_summary: list[dict[str, object]] = []
    for strategy_name in sorted({str(row["strategy"]) for row in simulation_rows}):
        subset = [row for row in simulation_rows if row["strategy"] == strategy_name]
        values = [float(row["strategy_value_index"]) for row in subset]
        growth_rates = [float(row["growth_rate"]) for row in subset]

        simulation_summary.append({
            "strategy": strategy_name,
            "final_value": round(values[-1], 6),
            "min_value": round(min(values), 6),
            "max_value": round(max(values), 6),
            "average_value": round(mean(values), 6),
            "value_volatility": round(stdev(values), 6),
            "average_growth_rate": round(mean(growth_rates), 6),
            "worst_growth_rate": round(min(growth_rates), 6),
        })

    simulation_summary = sorted(simulation_summary, key=lambda row: float(row["final_value"]), reverse=True)

    write_csv(TABLES / "dmdu_strategy_performance_matrix.csv", performance_rows)
    write_csv(TABLES / "dmdu_robustness_results_by_profile.csv", robustness)
    write_csv(TABLES / "dmdu_regret_matrix.csv", regrets)
    write_csv(TABLES / "dmdu_vulnerability_table.csv", vulnerabilities)
    write_csv(TABLES / "dmdu_scenario_summary.csv", scenario_rows)
    write_csv(TABLES / "dmdu_adaptive_strategy_simulation.csv", simulation_rows)
    write_csv(TABLES / "dmdu_adaptive_strategy_summary.csv", simulation_summary)
    write_csv(
        TABLES / "dmdu_ambiguity_profiles.csv",
        [
            {"profile": profile, "scenario": scenario, "weight": weight}
            for profile, weights in profiles.items()
            for scenario, weight in weights.items()
        ],
    )

    write_json(
        RECORDS / "deep_uncertainty_decision_record.json",
        {
            "article": "Decision-Making Under Deep Uncertainty",
            "decision_context": "Comparing strategies across ambiguous futures, contested scenario weights, regret profiles, vulnerability conditions, and adaptive performance.",
            "scenarios": scenarios,
            "ambiguity_profiles": profiles,
            "thresholds": thresholds,
            "robustness_results": robustness,
            "scenario_summary": scenario_rows,
            "adaptive_strategy_summary": simulation_summary,
            "modeling_principles": [
                "Deep uncertainty occurs when models, probabilities, futures, or values are contested.",
                "Strategies should be tested across plausible futures rather than optimized for one forecast.",
                "Robustness, regret, threshold compliance, and vulnerability sets reveal different kinds of decision fragility.",
                "Adaptive strategies preserve revision capacity as evidence changes.",
                "Decision records should preserve assumptions, scenarios, thresholds, trade-offs, and review triggers."
            ],
        },
    )

    print("Decision-making under deep uncertainty workflow complete.")
    print(TABLES / "dmdu_robustness_results_by_profile.csv")
    print(TABLES / "dmdu_adaptive_strategy_summary.csv")
    print(RECORDS / "deep_uncertainty_decision_record.json")


if __name__ == "__main__":
    main()
