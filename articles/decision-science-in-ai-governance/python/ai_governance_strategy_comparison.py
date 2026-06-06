#!/usr/bin/env python3
"""AI governance option comparison workflow."""

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
    options = read_csv_dicts(DATA / "synthetic_ai_governance_options.csv")
    probabilities = scenario_probabilities()
    results: list[dict[str, object]] = []

    for row in options:
        values = {
            "baseline_value": float(row["baseline_value"]),
            "safety_stress": float(row["safety_stress"]),
            "equity_stress": float(row["equity_stress"]),
            "security_stress": float(row["security_stress"]),
            "drift_stress": float(row["drift_stress"]),
        }

        expected_governance_value = sum(values[name] * probabilities[name] for name in values)
        worst_case_value = min(values.values())
        scenario_dispersion = pstdev(list(values.values()))

        evidence_quality = float(row["evidence_quality"])
        oversight_strength = float(row["oversight_strength"])
        equity_score = float(row["equity_score"])
        transparency_score = float(row["transparency_score"])
        security_readiness = float(row["security_readiness"])
        implementation_feasibility = float(row["implementation_feasibility"])

        ai_governance_score = (
            0.20 * expected_governance_value / 100.0
            + 0.18 * worst_case_value / 100.0
            - 0.08 * scenario_dispersion / 30.0
            + 0.14 * evidence_quality
            + 0.14 * oversight_strength
            + 0.12 * equity_score
            + 0.10 * transparency_score
            + 0.08 * security_readiness
            + 0.06 * implementation_feasibility
        )

        review = (
            worst_case_value < 50.0
            or evidence_quality < 0.60
            or oversight_strength < 0.60
            or equity_score < 0.55
            or security_readiness < 0.55
        )

        results.append({
            "option": row["option"],
            "expected_governance_value": round(expected_governance_value, 6),
            "worst_case_value": round(worst_case_value, 6),
            "scenario_dispersion": round(scenario_dispersion, 6),
            "evidence_quality": evidence_quality,
            "oversight_strength": oversight_strength,
            "equity_score": equity_score,
            "transparency_score": transparency_score,
            "security_readiness": security_readiness,
            "implementation_feasibility": implementation_feasibility,
            "ai_governance_score": round(ai_governance_score, 6),
            "review_flag": "review" if review else "acceptable",
        })

    results = sorted(results, key=lambda item: float(item["ai_governance_score"]), reverse=True)
    for rank, row in enumerate(results, start=1):
        row["rank"] = rank

    write_csv(TABLES / "ai_governance_decision_results.csv", results)
    print(TABLES / "ai_governance_decision_results.csv")


if __name__ == "__main__":
    main()
