#!/usr/bin/env python3
"""Decision governance design comparison workflow."""

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
    designs = read_csv_dicts(DATA / "synthetic_governance_designs.csv")
    results: list[dict[str, object]] = []

    for row in designs:
        decision_quality = float(row["decision_quality"])
        legitimacy = float(row["legitimacy"])
        accountability = float(row["accountability"])
        implementation = float(row["implementation_reliability"])
        traceability = float(row["evidence_traceability"])
        review_strength = float(row["review_strength"])
        monitoring = float(row["monitoring_strength"])
        corrective = float(row["corrective_capacity"])
        risk = float(row["risk_exposure"])
        burden = float(row["process_burden"])

        governance_score = (
            0.16 * decision_quality
            + 0.14 * legitimacy
            + 0.16 * accountability
            + 0.12 * implementation
            + 0.10 * traceability
            + 0.10 * review_strength
            + 0.10 * monitoring
            + 0.10 * corrective
            - 0.08 * risk
            - 0.04 * burden
        )

        review_flag = (
            accountability < 0.60
            or traceability < 0.60
            or review_strength < 0.60
            or corrective < 0.60
            or risk > 0.60
        )

        results.append({
            "design": row["design"],
            "decision_quality": decision_quality,
            "legitimacy": legitimacy,
            "accountability": accountability,
            "implementation_reliability": implementation,
            "evidence_traceability": traceability,
            "review_strength": review_strength,
            "monitoring_strength": monitoring,
            "corrective_capacity": corrective,
            "risk_exposure": risk,
            "process_burden": burden,
            "governance_score": round(governance_score, 6),
            "review_flag": "review" if review_flag else "acceptable",
        })

    results.sort(key=lambda item: float(item["governance_score"]), reverse=True)
    for rank, row in enumerate(results, start=1):
        row["rank"] = rank

    write_csv(TABLES / "decision_governance_design_results.csv", results)
    print(TABLES / "decision_governance_design_results.csv")


if __name__ == "__main__":
    main()
