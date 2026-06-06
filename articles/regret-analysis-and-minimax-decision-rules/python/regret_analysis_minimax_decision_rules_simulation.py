#!/usr/bin/env python3
"""
Regret Analysis and Minimax Decision Rules workflow.

Compares strategies using payoff matrices, regret matrices, expected value,
maximin, minimax regret, threshold compliance, vulnerability analysis,
decision-rule winners, and decision-record export.

Uses only the Python standard library.
"""

from __future__ import annotations

from pathlib import Path
import csv
import json
from statistics import mean

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
    weights = {row["scenario"]: float(row["weight"]) for row in read_csv_dicts(DATA / "synthetic_scenarios.csv")}
    ensure_weights(weights)
    return weights


def load_payoff_matrix() -> list[dict[str, object]]:
    scenarios = load_scenarios()
    rows = read_csv_dicts(DATA / "synthetic_payoff_matrix.csv")
    output: list[dict[str, object]] = []

    for row in rows:
        item: dict[str, object] = {"strategy": row["strategy"]}
        for scenario in scenarios:
            item[scenario] = float(row[scenario])
        output.append(item)

    return output


def load_thresholds() -> dict[str, float]:
    return {
        row["threshold_name"]: float(row["value"])
        for row in read_csv_dicts(DATA / "synthetic_thresholds.csv")
    }


def ensure_weights(weights: dict[str, float]) -> None:
    total = sum(weights.values())
    if abs(total - 1.0) > 1e-9:
        raise ValueError(f"Scenario weights must sum to 1. Got {total}.")


def scenario_bests(payoff_rows: list[dict[str, object]], scenarios: list[str]) -> dict[str, float]:
    return {
        scenario: max(float(row[scenario]) for row in payoff_rows)
        for scenario in scenarios
    }


def compute_regret_matrix(payoff_rows: list[dict[str, object]], scenarios: list[str]) -> list[dict[str, object]]:
    bests = scenario_bests(payoff_rows, scenarios)
    output: list[dict[str, object]] = []

    for row in payoff_rows:
        item: dict[str, object] = {"strategy": row["strategy"]}
        for scenario in scenarios:
            item[scenario] = round(bests[scenario] - float(row[scenario]), 6)
        output.append(item)

    return output


def compute_vulnerability_table(payoff_rows: list[dict[str, object]], scenarios: list[str], threshold: float) -> list[dict[str, object]]:
    output: list[dict[str, object]] = []

    for row in payoff_rows:
        item: dict[str, object] = {"strategy": row["strategy"]}
        for scenario in scenarios:
            item[scenario] = float(row[scenario]) < threshold
        output.append(item)

    return output


def rank_values(rows: list[dict[str, object]], score_field: str, reverse: bool) -> dict[str, int]:
    ranked = sorted(rows, key=lambda row: float(row[score_field]), reverse=reverse)
    return {str(row["strategy"]): rank for rank, row in enumerate(ranked, start=1)}


def compute_decision_rule_comparison() -> list[dict[str, object]]:
    scenarios = load_scenarios()
    weights = load_scenario_weights()
    payoff_rows = load_payoff_matrix()
    thresholds = load_thresholds()
    performance_threshold = thresholds["minimum_acceptable_performance"]
    high_regret_threshold = thresholds["high_regret_threshold"]
    low_worst_case_threshold = thresholds["low_worst_case_threshold"]
    low_pass_rate_threshold = thresholds["low_pass_rate_threshold"]

    bests = scenario_bests(payoff_rows, scenarios)
    rows: list[dict[str, object]] = []

    for strategy in payoff_rows:
        payoffs = [float(strategy[scenario]) for scenario in scenarios]
        regrets = [bests[scenario] - float(strategy[scenario]) for scenario in scenarios]

        expected_value = sum(float(strategy[scenario]) * weights[scenario] for scenario in scenarios)
        maximin_value = min(payoffs)
        best_case = max(payoffs)
        performance_range = best_case - maximin_value
        average_regret = mean(regrets)
        maximum_regret = max(regrets)
        threshold_pass_rate = sum(1 for value in payoffs if value >= performance_threshold) / len(payoffs)
        vulnerability_count = sum(1 for value in payoffs if value < performance_threshold)

        combined_score = (
            0.25 * maximin_value
            + 0.25 * (1 - maximum_regret)
            + 0.25 * threshold_pass_rate
            + 0.15 * expected_value
            + 0.10 * (1 - performance_range)
        )

        review = (
            maximin_value < low_worst_case_threshold
            or maximum_regret > high_regret_threshold
            or threshold_pass_rate < low_pass_rate_threshold
        )

        rows.append({
            "strategy": strategy["strategy"],
            "expected_value": round(expected_value, 6),
            "maximin_value": round(maximin_value, 6),
            "best_case": round(best_case, 6),
            "performance_range": round(performance_range, 6),
            "average_regret": round(average_regret, 6),
            "maximum_regret": round(maximum_regret, 6),
            "threshold_pass_rate": round(threshold_pass_rate, 6),
            "vulnerability_count": vulnerability_count,
            "combined_robustness_score": round(combined_score, 6),
            "review_flag": "review" if review else "acceptable",
        })

    rank_maps = {
        "expected_value_rank": rank_values(rows, "expected_value", True),
        "maximin_rank": rank_values(rows, "maximin_value", True),
        "minimax_regret_rank": rank_values(rows, "maximum_regret", False),
        "threshold_rank": rank_values(rows, "threshold_pass_rate", True),
        "combined_rank": rank_values(rows, "combined_robustness_score", True),
    }

    output: list[dict[str, object]] = []
    for row in rows:
        item = dict(row)
        for key, rank_map in rank_maps.items():
            item[key] = rank_map[str(row["strategy"])]
        output.append(item)

    return sorted(output, key=lambda row: int(row["combined_rank"]))


def decision_rule_winners(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {"rule": "Expected value", "selected_strategy": min(rows, key=lambda row: int(row["expected_value_rank"]))["strategy"]},
        {"rule": "Maximin", "selected_strategy": min(rows, key=lambda row: int(row["maximin_rank"]))["strategy"]},
        {"rule": "Minimax regret", "selected_strategy": min(rows, key=lambda row: int(row["minimax_regret_rank"]))["strategy"]},
        {"rule": "Threshold pass rate", "selected_strategy": min(rows, key=lambda row: int(row["threshold_rank"]))["strategy"]},
        {"rule": "Combined robustness", "selected_strategy": min(rows, key=lambda row: int(row["combined_rank"]))["strategy"]},
    ]


def scenario_summary(payoff_rows: list[dict[str, object]], scenarios: list[str]) -> list[dict[str, object]]:
    output: list[dict[str, object]] = []

    for scenario in scenarios:
        values = [(row["strategy"], float(row[scenario])) for row in payoff_rows]
        best_strategy, best_value = max(values, key=lambda item: item[1])
        worst_strategy, worst_value = min(values, key=lambda item: item[1])
        output.append({
            "scenario": scenario,
            "best_strategy": best_strategy,
            "best_value": round(best_value, 6),
            "worst_strategy": worst_strategy,
            "worst_value": round(worst_value, 6),
            "scenario_spread": round(best_value - worst_value, 6),
        })

    return output


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
    weights = load_scenario_weights()
    thresholds = load_thresholds()
    payoff_rows = load_payoff_matrix()
    regret_rows = compute_regret_matrix(payoff_rows, scenarios)
    vulnerability_rows = compute_vulnerability_table(payoff_rows, scenarios, thresholds["minimum_acceptable_performance"])
    comparison = compute_decision_rule_comparison()
    winners = decision_rule_winners(comparison)
    scenario_rows = scenario_summary(payoff_rows, scenarios)

    write_csv(TABLES / "regret_payoff_matrix.csv", payoff_rows)
    write_csv(TABLES / "regret_scenario_weights.csv", [{"scenario": k, "weight": v} for k, v in weights.items()])
    write_csv(TABLES / "regret_matrix.csv", regret_rows)
    write_csv(TABLES / "regret_vulnerability_table.csv", vulnerability_rows)
    write_csv(TABLES / "regret_decision_rule_comparison.csv", comparison)
    write_csv(TABLES / "regret_decision_rule_winners.csv", winners)
    write_csv(TABLES / "regret_scenario_summary.csv", scenario_rows)

    write_json(
        RECORDS / "regret_analysis_decision_record.json",
        {
            "article": "Regret Analysis and Minimax Decision Rules",
            "decision_context": "Comparing strategies across uncertain scenarios using expected value, maximin, minimax regret, threshold compliance, and vulnerability analysis.",
            "scenarios": scenarios,
            "scenario_weights": weights,
            "thresholds": thresholds,
            "decision_rule_comparison": comparison,
            "decision_rule_winners": winners,
            "scenario_summary": scenario_rows,
            "modeling_principles": [
                "Regret measures opportunity loss relative to the hindsight-best action in each state.",
                "Maximin protects the worst absolute payoff.",
                "Minimax regret protects against the worst missed opportunity.",
                "Expected value requires credible probabilities.",
                "Regret should be evaluated alongside absolute thresholds and vulnerability sets."
            ],
        },
    )

    print("Regret analysis and minimax decision rules workflow complete.")
    print(TABLES / "regret_decision_rule_comparison.csv")
    print(TABLES / "regret_decision_rule_winners.csv")
    print(RECORDS / "regret_analysis_decision_record.json")


if __name__ == "__main__":
    main()
