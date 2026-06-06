#!/usr/bin/env python3
"""Robust Decision-Making workflow using only the Python standard library."""

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


def load_scenario_weights() -> dict[str, float]:
    rows = read_csv_dicts(DATA / "synthetic_scenarios.csv")
    weights = {row["scenario"]: float(row["weight"]) for row in rows}
    total = sum(weights.values())
    if abs(total - 1.0) > 1e-9:
        raise ValueError(f"Scenario weights must sum to 1. Got {total}.")
    return weights


def load_performance_matrix() -> list[dict[str, object]]:
    rows = read_csv_dicts(DATA / "synthetic_performance_matrix.csv")
    scenarios = load_scenarios()
    output: list[dict[str, object]] = []
    for row in rows:
        item: dict[str, object] = {"strategy": row["strategy"]}
        for scenario in scenarios:
            item[scenario] = float(row[scenario])
        output.append(item)
    return output


def load_strategy_parameters() -> dict[str, dict[str, float]]:
    rows = read_csv_dicts(DATA / "synthetic_strategies.csv")
    return {
        row["strategy"]: {
            "base_return": float(row["base_return"]),
            "volatility": float(row["volatility"]),
            "adaptability": float(row["adaptability"]),
            "resilience": float(row["resilience"]),
        }
        for row in rows
    }


def load_thresholds() -> dict[str, float]:
    rows = read_csv_dicts(DATA / "synthetic_thresholds.csv")
    return {row["threshold_name"]: float(row["value"]) for row in rows}


def rank_rows(rows: list[dict[str, object]], score_field: str) -> list[dict[str, object]]:
    output = []
    for rank, row in enumerate(sorted(rows, key=lambda x: float(x[score_field]), reverse=True), start=1):
        item = dict(row)
        item["rank"] = rank
        output.append(item)
    return output


def compute_robustness_results() -> list[dict[str, object]]:
    scenarios = load_scenarios()
    scenario_weights = load_scenario_weights()
    performance_rows = load_performance_matrix()
    thresholds = load_thresholds()
    threshold = thresholds["minimum_acceptable_performance"]
    scenario_maxima = {scenario: max(float(row[scenario]) for row in performance_rows) for scenario in scenarios}
    rows = []

    for strategy in performance_rows:
        performances = [float(strategy[scenario]) for scenario in scenarios]
        regrets = [scenario_maxima[scenario] - float(strategy[scenario]) for scenario in scenarios]
        expected_value = sum(float(strategy[scenario]) * scenario_weights[scenario] for scenario in scenarios)
        worst_case = min(performances)
        best_case = max(performances)
        performance_range = best_case - worst_case
        average_regret = mean(regrets)
        max_regret = max(regrets)
        pass_rate = sum(1 for value in performances if value >= threshold) / len(performances)
        vulnerability_count = sum(1 for value in performances if value < threshold)
        robustness_score = (
            0.30 * worst_case
            + 0.25 * pass_rate
            + 0.20 * (1 - max_regret)
            + 0.15 * expected_value
            + 0.10 * (1 - performance_range)
        )
        review = (
            worst_case < thresholds["low_worst_case_threshold"]
            or max_regret > thresholds["high_regret_threshold"]
            or pass_rate < thresholds["low_pass_rate_threshold"]
        )
        rows.append({
            "strategy": strategy["strategy"],
            "expected_value": round(expected_value, 6),
            "worst_case": round(worst_case, 6),
            "best_case": round(best_case, 6),
            "performance_range": round(performance_range, 6),
            "average_regret": round(average_regret, 6),
            "max_regret": round(max_regret, 6),
            "threshold_pass_rate": round(pass_rate, 6),
            "vulnerability_count": vulnerability_count,
            "robustness_score": round(robustness_score, 6),
            "review_flag": "review" if review else "acceptable",
        })
    return rank_rows(rows, "robustness_score")


def compute_regret_matrix(performance_rows: list[dict[str, object]], scenarios: list[str]) -> list[dict[str, object]]:
    scenario_maxima = {scenario: max(float(row[scenario]) for row in performance_rows) for scenario in scenarios}
    rows = []
    for row in performance_rows:
        item: dict[str, object] = {"strategy": row["strategy"]}
        for scenario in scenarios:
            item[scenario] = round(scenario_maxima[scenario] - float(row[scenario]), 6)
        rows.append(item)
    return rows


def compute_vulnerability_table(performance_rows: list[dict[str, object]], scenarios: list[str], threshold: float) -> list[dict[str, object]]:
    rows = []
    for row in performance_rows:
        item: dict[str, object] = {"strategy": row["strategy"]}
        for scenario in scenarios:
            item[scenario] = float(row[scenario]) < threshold
        rows.append(item)
    return rows


def simulate_strategy(strategy_name: str, params: dict[str, float], time_steps: int, rng: random.Random) -> list[dict[str, object]]:
    value = 100.0
    rows = []
    for time in range(1, time_steps + 1):
        regime_shift = rng.choices([-2.8, -1.2, 0.0, 1.0, 2.1], weights=[0.10, 0.20, 0.30, 0.25, 0.15], k=1)[0]
        shock = rng.gauss(0.0, params["volatility"])
        adaptive_buffer = params["adaptability"] * rng.uniform(0.4, 1.3)
        resilience_buffer = params["resilience"] * rng.uniform(0.3, 1.0)
        growth = params["base_return"] + regime_shift + shock + adaptive_buffer + resilience_buffer
        value = max(20.0, value * (1.0 + growth / 100.0))
        rows.append({
            "strategy": strategy_name,
            "time": time,
            "strategy_value_index": round(value, 6),
            "growth_rate": round(growth, 6),
            "regime_shift": round(regime_shift, 6),
            "shock": round(shock, 6),
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
    scenario_weights = load_scenario_weights()
    performance_rows = load_performance_matrix()
    thresholds = load_thresholds()
    strategy_parameters = load_strategy_parameters()
    robustness_results = compute_robustness_results()
    regret_rows = compute_regret_matrix(performance_rows, scenarios)
    vulnerability_rows = compute_vulnerability_table(performance_rows, scenarios, thresholds["minimum_acceptable_performance"])

    scenario_summary = []
    for scenario in scenarios:
        values = [(row["strategy"], float(row[scenario])) for row in performance_rows]
        best_strategy, max_performance = max(values, key=lambda item: item[1])
        _, min_performance = min(values, key=lambda item: item[1])
        scenario_summary.append({
            "scenario": scenario,
            "best_strategy": best_strategy,
            "max_performance": round(max_performance, 6),
            "min_performance": round(min_performance, 6),
            "scenario_spread": round(max_performance - min_performance, 6),
        })

    rng = random.Random(42)
    simulation_rows = []
    for strategy_name, params in strategy_parameters.items():
        simulation_rows.extend(simulate_strategy(strategy_name, params, time_steps=40, rng=rng))

    simulation_summary = []
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

    write_csv(TABLES / "rdm_strategy_performance_matrix.csv", performance_rows)
    write_csv(TABLES / "rdm_scenario_weights.csv", [{"scenario": key, "weight": value} for key, value in scenario_weights.items()])
    write_csv(TABLES / "rdm_robustness_results.csv", robustness_results)
    write_csv(TABLES / "rdm_regret_matrix.csv", regret_rows)
    write_csv(TABLES / "rdm_vulnerability_table.csv", vulnerability_rows)
    write_csv(TABLES / "rdm_scenario_summary.csv", scenario_summary)
    write_csv(TABLES / "rdm_strategy_durability_simulation.csv", simulation_rows)
    write_csv(TABLES / "rdm_strategy_durability_summary.csv", simulation_summary)

    write_json(RECORDS / "robust_decision_record.json", {
        "article": "Robust Decision-Making",
        "decision_context": "Comparing strategies across uncertain futures using expected value, worst-case performance, regret, threshold compliance, vulnerabilities, and durability under uncertainty shocks.",
        "scenarios": scenarios,
        "scenario_weights": scenario_weights,
        "thresholds": thresholds,
        "robustness_results": robustness_results,
        "scenario_summary": scenario_summary,
        "durability_summary": simulation_summary,
        "modeling_principles": [
            "Robust decision-making evaluates strategies across many plausible futures.",
            "Expected value is useful but insufficient under deep uncertainty.",
            "Worst-case performance, regret, and threshold compliance reveal brittleness.",
            "Adaptive strategies can preserve flexibility as uncertainty unfolds.",
            "Decision records should document scenarios, thresholds, vulnerabilities, triggers, and review responsibilities."
        ],
    })

    print("Robust decision-making workflow complete.")
    print(TABLES / "rdm_robustness_results.csv")
    print(TABLES / "rdm_strategy_durability_summary.csv")
    print(RECORDS / "robust_decision_record.json")


if __name__ == "__main__":
    main()
