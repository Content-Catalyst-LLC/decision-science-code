#!/usr/bin/env python3
"""Adaptive pathway comparison workflow."""

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


def adaptive_pathway_score(row: dict[str, str]) -> float:
    return (
        0.20 * float(row["initial_performance"])
        + 0.18 * float(row["flexibility"])
        + 0.16 * float(row["monitoring_quality"])
        + 0.16 * float(row["trigger_clarity"])
        - 0.12 * float(row["switching_cost"])
        + 0.18 * float(row["fallback_strength"])
    )


def scenario_summary() -> dict[str, dict[str, float]]:
    rows = read_csv_dicts(DATA / "synthetic_scenario_performance.csv")
    by_pathway: dict[str, list[float]] = {}

    for row in rows:
        by_pathway.setdefault(row["pathway"], []).append(float(row["performance"]))

    return {
        pathway: {
            "average_performance": mean(values),
            "worst_case_performance": min(values),
            "performance_range": max(values) - min(values),
            "threshold_pass_rate": sum(1 for value in values if value >= 0.70) / len(values),
        }
        for pathway, values in by_pathway.items()
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
    profiles = read_csv_dicts(DATA / "synthetic_pathway_profiles.csv")
    scenarios = scenario_summary()

    results: list[dict[str, object]] = []

    for row in profiles:
        pathway = row["pathway"]
        base_score = adaptive_pathway_score(row)
        scenario = scenarios[pathway]

        robust_adaptive_score = (
            0.30 * base_score
            + 0.24 * scenario["average_performance"]
            + 0.22 * scenario["worst_case_performance"]
            + 0.18 * scenario["threshold_pass_rate"]
            - 0.06 * scenario["performance_range"]
        )

        review = (
            float(row["trigger_clarity"]) < 0.45
            or float(row["monitoring_quality"]) < 0.45
            or float(row["switching_cost"]) > 0.70
            or float(row["fallback_strength"]) < 0.45
            or scenario["worst_case_performance"] < 0.60
            or scenario["threshold_pass_rate"] < 0.60
        )

        results.append({
            "pathway": pathway,
            "adaptive_pathway_score": round(base_score, 6),
            "average_performance": round(scenario["average_performance"], 6),
            "worst_case_performance": round(scenario["worst_case_performance"], 6),
            "performance_range": round(scenario["performance_range"], 6),
            "threshold_pass_rate": round(scenario["threshold_pass_rate"], 6),
            "robust_adaptive_score": round(robust_adaptive_score, 6),
            "review_flag": "review" if review else "acceptable",
        })

    results = sorted(results, key=lambda item: float(item["robust_adaptive_score"]), reverse=True)
    for rank, row in enumerate(results, start=1):
        row["rank"] = rank

    write_csv(TABLES / "adaptive_pathway_decision_results.csv", results)
    print(TABLES / "adaptive_pathway_decision_results.csv")


if __name__ == "__main__":
    main()
