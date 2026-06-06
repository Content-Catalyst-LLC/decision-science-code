#!/usr/bin/env python3
"""Path strategy comparison workflow for path dependence and decision timing."""

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


def path_quality_score(row: dict[str, str]) -> float:
    return (
        0.24 * float(row["initial_value"])
        + 0.24 * float(row["future_flexibility"])
        - 0.16 * float(row["switching_cost"])
        - 0.18 * float(row["lock_in_risk"])
        + 0.14 * float(row["reversibility"])
        - 0.04 * float(row["timing_sensitivity"])
    )


def scenario_summary() -> dict[str, dict[str, float]]:
    rows = read_csv_dicts(DATA / "synthetic_scenario_performance.csv")
    by_path: dict[str, list[float]] = {}

    for row in rows:
        by_path.setdefault(row["path"], []).append(float(row["performance"]))

    return {
        path: {
            "average_scenario_performance": mean(values),
            "worst_case_performance": min(values),
            "performance_range": max(values) - min(values),
            "threshold_pass_rate": sum(1 for value in values if value >= 0.70) / len(values),
        }
        for path, values in by_path.items()
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
    profiles = read_csv_dicts(DATA / "synthetic_path_profiles.csv")
    scenarios = scenario_summary()

    results: list[dict[str, object]] = []

    for row in profiles:
        path_name = row["path"]
        base_score = path_quality_score(row)
        scenario = scenarios[path_name]

        timing_adjusted_score = (
            0.30 * base_score
            + 0.24 * scenario["average_scenario_performance"]
            + 0.22 * scenario["worst_case_performance"]
            + 0.18 * scenario["threshold_pass_rate"]
            - 0.06 * scenario["performance_range"]
        )

        review = (
            float(row["switching_cost"]) > 0.65
            or float(row["lock_in_risk"]) > 0.70
            or float(row["reversibility"]) < 0.35
            or scenario["worst_case_performance"] < 0.55
            or scenario["threshold_pass_rate"] < 0.60
        )

        results.append({
            "path": path_name,
            "path_quality_score": round(base_score, 6),
            "average_scenario_performance": round(scenario["average_scenario_performance"], 6),
            "worst_case_performance": round(scenario["worst_case_performance"], 6),
            "performance_range": round(scenario["performance_range"], 6),
            "threshold_pass_rate": round(scenario["threshold_pass_rate"], 6),
            "timing_adjusted_score": round(timing_adjusted_score, 6),
            "review_flag": "review" if review else "acceptable",
        })

    results = sorted(results, key=lambda item: float(item["timing_adjusted_score"]), reverse=True)
    for rank, row in enumerate(results, start=1):
        row["rank"] = rank

    write_csv(TABLES / "path_dependence_decision_results.csv", results)
    print(TABLES / "path_dependence_decision_results.csv")


if __name__ == "__main__":
    main()
