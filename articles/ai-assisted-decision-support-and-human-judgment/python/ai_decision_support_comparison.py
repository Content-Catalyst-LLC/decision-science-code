#!/usr/bin/env python3
"""AI decision-support design comparison workflow."""

from __future__ import annotations

from pathlib import Path
import csv

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
    designs = read_csv_dicts(DATA / "synthetic_ai_support_designs.csv")
    results: list[dict[str, object]] = []

    for row in designs:
        model_performance = float(row["model_performance"])
        uncertainty_visibility = float(row["uncertainty_visibility"])
        human_oversight = float(row["human_oversight"])
        contestability = float(row["contestability"])
        fairness_review = float(row["fairness_review"])
        accountability = float(row["accountability"])
        monitoring = float(row["monitoring_strength"])
        automation_bias = float(row["automation_bias_risk"])
        burden = float(row["process_burden"])

        decision_support_score = (
            0.16 * model_performance
            + 0.14 * uncertainty_visibility
            + 0.16 * human_oversight
            + 0.14 * contestability
            + 0.14 * fairness_review
            + 0.14 * accountability
            + 0.10 * monitoring
            - 0.10 * automation_bias
            - 0.04 * burden
        )

        review_flag = (
            human_oversight < 0.60
            or contestability < 0.60
            or fairness_review < 0.60
            or accountability < 0.60
            or automation_bias > 0.60
        )

        results.append({
            "design": row["design"],
            "model_performance": model_performance,
            "uncertainty_visibility": uncertainty_visibility,
            "human_oversight": human_oversight,
            "contestability": contestability,
            "fairness_review": fairness_review,
            "accountability": accountability,
            "monitoring_strength": monitoring,
            "automation_bias_risk": automation_bias,
            "process_burden": burden,
            "decision_support_score": round(decision_support_score, 6),
            "review_flag": "review" if review_flag else "acceptable",
        })

    results.sort(key=lambda item: float(item["decision_support_score"]), reverse=True)
    for rank, row in enumerate(results, start=1):
        row["rank"] = rank

    write_csv(TABLES / "ai_decision_support_design_results.csv", results)
    print(TABLES / "ai_decision_support_design_results.csv")


if __name__ == "__main__":
    main()
