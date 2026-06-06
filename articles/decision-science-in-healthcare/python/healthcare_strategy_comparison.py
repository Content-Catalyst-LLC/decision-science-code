#!/usr/bin/env python3
"""Healthcare treatment strategy comparison workflow."""

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


def treatment_value_score(row: dict[str, str]) -> float:
    return (
        0.30 * float(row["expected_benefit"])
        - 0.18 * float(row["adverse_event_risk"])
        - 0.14 * float(row["cost_burden"])
        + 0.18 * float(row["patient_preference_fit"])
        + 0.10 * float(row["equity_score"])
        + 0.10 * float(row["implementation_feasibility"])
    )


def scenario_summary() -> dict[str, dict[str, float]]:
    rows = read_csv_dicts(DATA / "synthetic_scenario_performance.csv")
    by_treatment: dict[str, list[float]] = {}

    for row in rows:
        by_treatment.setdefault(row["treatment"], []).append(float(row["performance"]))

    return {
        treatment: {
            "average_performance": mean(values),
            "worst_case_performance": min(values),
            "performance_range": max(values) - min(values),
            "threshold_pass_rate": sum(1 for value in values if value >= 0.65) / len(values),
        }
        for treatment, values in by_treatment.items()
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
    profiles = read_csv_dicts(DATA / "synthetic_treatment_profiles.csv")
    scenarios = scenario_summary()

    results: list[dict[str, object]] = []

    for row in profiles:
        treatment = row["treatment"]
        base_score = treatment_value_score(row)
        scenario = scenarios[treatment]

        robust_score = (
            0.34 * base_score
            + 0.24 * scenario["average_performance"]
            + 0.22 * scenario["worst_case_performance"]
            + 0.14 * scenario["threshold_pass_rate"]
            - 0.06 * scenario["performance_range"]
        )

        review = (
            float(row["adverse_event_risk"]) > 0.25
            or float(row["patient_preference_fit"]) < 0.60
            or float(row["equity_score"]) < 0.55
            or float(row["implementation_feasibility"]) < 0.55
            or scenario["worst_case_performance"] < 0.50
            or scenario["threshold_pass_rate"] < 0.60
        )

        results.append({
            "treatment": treatment,
            "treatment_value_score": round(base_score, 6),
            "average_performance": round(scenario["average_performance"], 6),
            "worst_case_performance": round(scenario["worst_case_performance"], 6),
            "performance_range": round(scenario["performance_range"], 6),
            "threshold_pass_rate": round(scenario["threshold_pass_rate"], 6),
            "robust_healthcare_score": round(robust_score, 6),
            "review_flag": "review" if review else "acceptable",
        })

    results = sorted(results, key=lambda item: float(item["robust_healthcare_score"]), reverse=True)
    for rank, row in enumerate(results, start=1):
        row["rank"] = rank

    write_csv(TABLES / "healthcare_decision_results.csv", results)
    print(TABLES / "healthcare_decision_results.csv")


if __name__ == "__main__":
    main()
