#!/usr/bin/env python3
"""Strategic option comparison workflow."""

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
    profiles = read_csv_dicts(DATA / "synthetic_strategy_profiles.csv")
    probs = scenario_probabilities()

    results: list[dict[str, object]] = []

    for row in profiles:
        values = {
            "low_growth": float(row["low_growth"]),
            "base_case": float(row["base_case"]),
            "high_growth": float(row["high_growth"]),
            "disruption": float(row["disruption"]),
        }

        expected_value = sum(values[name] * probs[name] for name in values)
        downside_robustness = min(values.values())
        scenario_dispersion = pstdev(list(values.values()))

        adaptability = float(row["adaptability"])
        capability_fit = float(row["capability_fit"])
        governance_feasibility = float(row["governance_feasibility"])
        reversibility = float(row["reversibility"])

        strategy_quality_score = (
            0.28 * expected_value / 100.0
            + 0.22 * downside_robustness / 100.0
            - 0.10 * scenario_dispersion / 30.0
            + 0.14 * adaptability
            + 0.12 * capability_fit
            + 0.08 * governance_feasibility
            + 0.06 * reversibility
        )

        review = (
            downside_robustness < 50.0
            or capability_fit < 0.55
            or governance_feasibility < 0.55
            or reversibility < 0.40
        )

        results.append({
            "strategy": row["strategy"],
            "expected_value": round(expected_value, 6),
            "downside_robustness": round(downside_robustness, 6),
            "scenario_dispersion": round(scenario_dispersion, 6),
            "adaptability": adaptability,
            "capability_fit": capability_fit,
            "governance_feasibility": governance_feasibility,
            "reversibility": reversibility,
            "strategy_quality_score": round(strategy_quality_score, 6),
            "review_flag": "review" if review else "acceptable",
        })

    results = sorted(results, key=lambda item: float(item["strategy_quality_score"]), reverse=True)
    for rank, row in enumerate(results, start=1):
        row["rank"] = rank

    write_csv(TABLES / "organizational_strategy_decision_profiles.csv", results)
    print(TABLES / "organizational_strategy_decision_profiles.csv")


if __name__ == "__main__":
    main()
