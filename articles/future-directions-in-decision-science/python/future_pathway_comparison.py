#!/usr/bin/env python3
"""Future decision-science pathway comparison workflow."""

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
    pathways = read_csv_dicts(DATA / "synthetic_future_pathways.csv")
    results: list[dict[str, object]] = []

    for row in pathways:
        ai_readiness = float(row["ai_readiness"])
        governance_maturity = float(row["governance_maturity"])
        uncertainty_capability = float(row["uncertainty_capability"])
        participatory_legitimacy = float(row["participatory_legitimacy"])
        reproducibility = float(row["reproducibility"])
        systems_modeling = float(row["systems_modeling"])
        ethical_accountability = float(row["ethical_accountability"])
        adaptive_capacity = float(row["adaptive_capacity"])
        process_burden = float(row["process_burden"])
        failure_risk = float(row["failure_risk"])

        score = (
            0.12 * ai_readiness
            + 0.14 * governance_maturity
            + 0.14 * uncertainty_capability
            + 0.12 * participatory_legitimacy
            + 0.12 * reproducibility
            + 0.12 * systems_modeling
            + 0.14 * ethical_accountability
            + 0.14 * adaptive_capacity
            - 0.04 * process_burden
            - 0.12 * failure_risk
        )

        review_flag = (
            governance_maturity < 0.60
            or uncertainty_capability < 0.60
            or ethical_accountability < 0.60
            or adaptive_capacity < 0.60
            or failure_risk > 0.55
        )

        results.append({
            "pathway": row["pathway"],
            "ai_readiness": ai_readiness,
            "governance_maturity": governance_maturity,
            "uncertainty_capability": uncertainty_capability,
            "participatory_legitimacy": participatory_legitimacy,
            "reproducibility": reproducibility,
            "systems_modeling": systems_modeling,
            "ethical_accountability": ethical_accountability,
            "adaptive_capacity": adaptive_capacity,
            "process_burden": process_burden,
            "failure_risk": failure_risk,
            "future_decision_score": round(score, 6),
            "review_flag": "review" if review_flag else "acceptable",
        })

    results.sort(key=lambda item: float(item["future_decision_score"]), reverse=True)
    for rank, row in enumerate(results, start=1):
        row["rank"] = rank

    write_csv(TABLES / "future_decision_science_pathways.csv", results)
    print(TABLES / "future_decision_science_pathways.csv")


if __name__ == "__main__":
    main()
