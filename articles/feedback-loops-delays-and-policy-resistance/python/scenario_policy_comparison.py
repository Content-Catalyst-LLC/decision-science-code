#!/usr/bin/env python3
"""Scenario policy comparison for feedback loops, delays, and policy resistance."""

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


def dynamic_policy_score(row: dict[str, str]) -> float:
    return (
        0.24 * float(row["balancing_correction"])
        - 0.18 * float(row["reinforcing_pressure"])
        - 0.18 * float(row["implementation_delay"])
        - 0.18 * float(row["resistance_intensity"])
        + 0.22 * float(row["monitoring_quality"])
    )


def scenario_summary() -> dict[str, dict[str, float]]:
    rows = read_csv_dicts(DATA / "synthetic_scenario_performance.csv")
    by_context: dict[str, list[float]] = {}

    for row in rows:
        by_context.setdefault(row["context"], []).append(float(row["performance"]))

    return {
        context: {
            "average_scenario_performance": mean(values),
            "worst_case_performance": min(values),
            "performance_range": max(values) - min(values),
            "threshold_pass_rate": sum(1 for value in values if value >= 0.70) / len(values),
        }
        for context, values in by_context.items()
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
    contexts = read_csv_dicts(DATA / "synthetic_policy_contexts.csv")
    scenarios = scenario_summary()

    results: list[dict[str, object]] = []

    for row in contexts:
        context = row["context"]
        base_score = dynamic_policy_score(row)
        scenario = scenarios[context]

        feedback_adjusted_score = (
            0.35 * base_score
            + 0.25 * scenario["average_scenario_performance"]
            + 0.20 * scenario["worst_case_performance"]
            + 0.20 * scenario["threshold_pass_rate"]
        )

        review = (
            float(row["reinforcing_pressure"]) > 0.75
            or float(row["implementation_delay"]) > 0.65
            or float(row["resistance_intensity"]) > 0.65
            or float(row["monitoring_quality"]) < 0.50
            or scenario["worst_case_performance"] < 0.60
        )

        results.append({
            "context": context,
            "dynamic_policy_score": round(base_score, 6),
            "average_scenario_performance": round(scenario["average_scenario_performance"], 6),
            "worst_case_performance": round(scenario["worst_case_performance"], 6),
            "performance_range": round(scenario["performance_range"], 6),
            "threshold_pass_rate": round(scenario["threshold_pass_rate"], 6),
            "feedback_adjusted_score": round(feedback_adjusted_score, 6),
            "review_flag": "review" if review else "acceptable",
        })

    results = sorted(results, key=lambda item: float(item["feedback_adjusted_score"]), reverse=True)
    for rank, row in enumerate(results, start=1):
        row["rank"] = rank

    write_csv(TABLES / "feedback_delay_policy_results.csv", results)
    print(TABLES / "feedback_delay_policy_results.csv")


if __name__ == "__main__":
    main()
