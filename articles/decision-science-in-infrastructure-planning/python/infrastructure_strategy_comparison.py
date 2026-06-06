#!/usr/bin/env python3
"""Infrastructure alternative comparison workflow."""

from __future__ import annotations

from pathlib import Path
import csv
from statistics import pstdev

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
DATA = ARTICLE_ROOT / "data"
TABLES = ARTICLE_ROOT / "outputs" / "tables"


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def scenario_probabilities() -> dict[str, float]:
    return {row["scenario"]: float(row["probability"]) for row in read_csv_dicts(DATA / "synthetic_scenarios.csv")}


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"No rows to write: {path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    alternatives = read_csv_dicts(DATA / "synthetic_infrastructure_alternatives.csv")
    probabilities = scenario_probabilities()
    results: list[dict[str, object]] = []

    for row in alternatives:
        values = {
            "baseline": float(row["baseline"]),
            "climate_stress": float(row["climate_stress"]),
            "demand_growth": float(row["demand_growth"]),
            "funding_constraint": float(row["funding_constraint"]),
            "disruption": float(row["disruption"]),
        }

        expected_service_value = sum(values[name] * probabilities[name] for name in values)
        worst_case_value = min(values.values())
        scenario_dispersion = pstdev(list(values.values()))

        lifecycle_cost = float(row["lifecycle_cost"])
        equity_score = float(row["equity_score"])
        resilience_score = float(row["resilience_score"])
        environmental_score = float(row["environmental_score"])
        implementation_feasibility = float(row["implementation_feasibility"])
        adaptability = float(row["adaptability"])

        infrastructure_decision_score = (
            0.22 * expected_service_value / 100.0
            + 0.20 * worst_case_value / 100.0
            - 0.10 * scenario_dispersion / 30.0
            - 0.12 * lifecycle_cost
            + 0.14 * equity_score
            + 0.14 * resilience_score
            + 0.10 * environmental_score
            + 0.06 * implementation_feasibility
            + 0.06 * adaptability
        )

        review = (
            worst_case_value < 50.0
            or equity_score < 0.55
            or resilience_score < 0.55
            or environmental_score < 0.50
            or implementation_feasibility < 0.50
        )

        results.append({
            "alternative": row["alternative"],
            "expected_service_value": round(expected_service_value, 6),
            "worst_case_value": round(worst_case_value, 6),
            "scenario_dispersion": round(scenario_dispersion, 6),
            "lifecycle_cost": lifecycle_cost,
            "equity_score": equity_score,
            "resilience_score": resilience_score,
            "environmental_score": environmental_score,
            "implementation_feasibility": implementation_feasibility,
            "adaptability": adaptability,
            "infrastructure_decision_score": round(infrastructure_decision_score, 6),
            "review_flag": "review" if review else "acceptable",
        })

    results = sorted(results, key=lambda item: float(item["infrastructure_decision_score"]), reverse=True)
    for rank, row in enumerate(results, start=1):
        row["rank"] = rank

    write_csv(TABLES / "infrastructure_decision_results.csv", results)
    print(TABLES / "infrastructure_decision_results.csv")


if __name__ == "__main__":
    main()
