#!/usr/bin/env python3
"""Crisis response option comparison workflow."""

from __future__ import annotations

from pathlib import Path
import csv
from statistics import pstdev

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
DATA = ARTICLE_ROOT / "data"
TABLES = ARTICLE_ROOT / "outputs" / "tables"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    options = read_csv(DATA / "synthetic_crisis_response_options.csv")
    probs = {row["scenario"]: float(row["probability"]) for row in read_csv(DATA / "synthetic_scenarios.csv")}
    results: list[dict[str, object]] = []

    for row in options:
        values = {
            "baseline": float(row["baseline"]),
            "rapid_escalation": float(row["rapid_escalation"]),
            "resource_constraint": float(row["resource_constraint"]),
            "public_trust_stress": float(row["public_trust_stress"]),
            "cascading_failure": float(row["cascading_failure"]),
        }
        expected = sum(values[k] * probs[k] for k in values)
        worst = min(values.values())
        dispersion = pstdev(list(values.values()))

        score = (
            0.22 * expected / 100
            + 0.20 * worst / 100
            - 0.08 * dispersion / 30
            + 0.12 * float(row["speed_score"])
            + 0.10 * float(row["feasibility_score"])
            + 0.14 * float(row["equity_score"])
            + 0.12 * float(row["trust_score"])
            + 0.10 * float(row["continuity_score"])
            + 0.10 * float(row["adaptability"])
        )

        review = (
            worst < 50
            or float(row["equity_score"]) < 0.55
            or float(row["trust_score"]) < 0.55
            or float(row["continuity_score"]) < 0.50
            or float(row["feasibility_score"]) < 0.50
        )

        results.append({
            "option": row["option"],
            "expected_response_value": round(expected, 6),
            "worst_case_value": round(worst, 6),
            "scenario_dispersion": round(dispersion, 6),
            "crisis_decision_score": round(score, 6),
            "speed_score": row["speed_score"],
            "feasibility_score": row["feasibility_score"],
            "equity_score": row["equity_score"],
            "trust_score": row["trust_score"],
            "continuity_score": row["continuity_score"],
            "adaptability": row["adaptability"],
            "review_flag": "review" if review else "acceptable",
        })

    results.sort(key=lambda item: float(item["crisis_decision_score"]), reverse=True)
    for rank, row in enumerate(results, start=1):
        row["rank"] = rank

    write_csv(TABLES / "crisis_response_decision_results.csv", results)
    print(TABLES / "crisis_response_decision_results.csv")


if __name__ == "__main__":
    main()
