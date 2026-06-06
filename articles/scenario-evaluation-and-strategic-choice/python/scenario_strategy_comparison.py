#!/usr/bin/env python3
"""Scenario strategy comparison workflow."""

from __future__ import annotations

from pathlib import Path
import csv
from statistics import mean, pstdev

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
DATA = ARTICLE_ROOT / "data"
TABLES = ARTICLE_ROOT / "outputs" / "tables"


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"No rows to write: {path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    scenario_rows = read_csv_dicts(DATA / "synthetic_scenarios.csv")
    performance_rows = read_csv_dicts(DATA / "synthetic_scenario_performance.csv")

    probabilities = {row["scenario"]: float(row["probability"]) for row in scenario_rows}
    scenarios = [row["scenario"] for row in scenario_rows]
    strategies = sorted({row["strategy"] for row in performance_rows})

    matrix: dict[str, dict[str, float]] = {strategy: {} for strategy in strategies}
    for row in performance_rows:
        matrix[row["strategy"]][row["scenario"]] = float(row["performance"])

    scenario_best: dict[str, float] = {
        scenario: max(matrix[strategy][scenario] for strategy in strategies)
        for scenario in scenarios
    }

    results: list[dict[str, object]] = []
    regret_rows: list[dict[str, object]] = []

    for strategy in strategies:
        values = [matrix[strategy][scenario] for scenario in scenarios]
        regrets = [scenario_best[scenario] - matrix[strategy][scenario] for scenario in scenarios]

        for scenario, value, regret in zip(scenarios, values, regrets):
            regret_rows.append({
                "strategy": strategy,
                "scenario": scenario,
                "performance": round(value, 6),
                "scenario_best": round(scenario_best[scenario], 6),
                "regret": round(regret, 6),
            })

        expected_value = sum(matrix[strategy][scenario] * probabilities[scenario] for scenario in scenarios)
        worst_case = min(values)
        threshold_pass_rate = sum(1 for value in values if value >= 0.70) / len(values)
        maximum_regret = max(regrets)
        dispersion = pstdev(values)

        robustness_score = (
            0.26 * expected_value
            + 0.24 * worst_case
            + 0.20 * threshold_pass_rate
            - 0.16 * maximum_regret
            - 0.14 * dispersion
        )

        review = worst_case < 0.55 or threshold_pass_rate < 0.60 or maximum_regret > 0.35

        results.append({
            "strategy": strategy,
            "expected_value": round(expected_value, 6),
            "worst_case": round(worst_case, 6),
            "average_performance": round(mean(values), 6),
            "scenario_dispersion": round(dispersion, 6),
            "maximum_regret": round(maximum_regret, 6),
            "threshold_pass_rate": round(threshold_pass_rate, 6),
            "scenario_robustness_score": round(robustness_score, 6),
            "review_flag": "review" if review else "acceptable",
        })

    results = sorted(results, key=lambda row: float(row["scenario_robustness_score"]), reverse=True)
    for rank, row in enumerate(results, start=1):
        row["rank"] = rank

    write_csv(TABLES / "scenario_evaluation_results.csv", results)
    write_csv(TABLES / "scenario_regret_table.csv", regret_rows)
    print(TABLES / "scenario_evaluation_results.csv")
    print(TABLES / "scenario_regret_table.csv")


if __name__ == "__main__":
    main()
