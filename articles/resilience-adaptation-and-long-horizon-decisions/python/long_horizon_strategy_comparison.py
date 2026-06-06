#!/usr/bin/env python3
"""Long-horizon strategy comparison for resilience and adaptation."""

from __future__ import annotations

from pathlib import Path
import csv
from statistics import mean

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
DATA = ARTICLE_ROOT / "data"
TABLES = ARTICLE_ROOT / "outputs" / "tables"


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def long_horizon_score(row: dict[str, str]) -> float:
    return (
        0.24 * float(row["resilience_score"])
        + 0.22 * float(row["adaptability_score"])
        - 0.12 * float(row["near_term_cost"])
        + 0.24 * float(row["long_term_value"])
        + 0.18 * float(row["reversibility"])
    )


def scenario_summary() -> dict[str, dict[str, float]]:
    rows = read_csv_dicts(DATA / "synthetic_scenario_performance.csv")
    by_strategy: dict[str, list[float]] = {}

    for row in rows:
        by_strategy.setdefault(row["strategy"], []).append(float(row["performance"]))

    return {
        strategy: {
            "average_scenario_performance": mean(values),
            "worst_case_performance": min(values),
            "performance_range": max(values) - min(values),
            "threshold_pass_rate": sum(1 for value in values if value >= 0.70) / len(values),
        }
        for strategy, values in by_strategy.items()
    }


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"No rows to write: {path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    profiles = read_csv_dicts(DATA / "synthetic_strategy_profiles.csv")
    scenarios = scenario_summary()

    results: list[dict[str, object]] = []

    for row in profiles:
        strategy = row["strategy"]
        base_score = long_horizon_score(row)
        scenario = scenarios[strategy]

        resilient_decision_score = (
            0.30 * base_score
            + 0.24 * scenario["average_scenario_performance"]
            + 0.22 * scenario["worst_case_performance"]
            + 0.18 * scenario["threshold_pass_rate"]
            - 0.06 * scenario["performance_range"]
        )

        review = (
            scenario["worst_case_performance"] < 0.60
            or scenario["threshold_pass_rate"] < 0.60
            or float(row["resilience_score"]) < 0.50
            or float(row["adaptability_score"]) < 0.50
        )

        results.append({
            "strategy": strategy,
            "long_horizon_score": round(base_score, 6),
            "average_scenario_performance": round(scenario["average_scenario_performance"], 6),
            "worst_case_performance": round(scenario["worst_case_performance"], 6),
            "performance_range": round(scenario["performance_range"], 6),
            "threshold_pass_rate": round(scenario["threshold_pass_rate"], 6),
            "resilient_decision_score": round(resilient_decision_score, 6),
            "review_flag": "review" if review else "acceptable",
        })

    results = sorted(results, key=lambda row: float(row["resilient_decision_score"]), reverse=True)
    for rank, row in enumerate(results, start=1):
        row["rank"] = rank

    write_csv(TABLES / "resilience_adaptation_decision_results.csv", results)
    print(TABLES / "resilience_adaptation_decision_results.csv")


if __name__ == "__main__":
    main()
