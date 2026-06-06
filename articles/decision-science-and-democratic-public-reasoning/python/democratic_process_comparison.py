#!/usr/bin/env python3
"""Democratic public reasoning process comparison workflow."""

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
    processes = read_csv_dicts(DATA / "synthetic_democratic_processes.csv")
    results: list[dict[str, object]] = []

    for row in processes:
        evidence_quality = float(row["evidence_quality"])
        transparency = float(row["transparency"])
        participation = float(row["participation"])
        procedural_fairness = float(row["procedural_fairness"])
        contestability = float(row["contestability"])
        equity_review = float(row["equity_review"])
        accountability = float(row["accountability"])
        uncertainty_communication = float(row["uncertainty_communication"])
        process_burden = float(row["process_burden"])
        public_trust_risk = float(row["public_trust_risk"])

        democratic_decision_quality = (
            0.14 * evidence_quality
            + 0.12 * transparency
            + 0.14 * participation
            + 0.14 * procedural_fairness
            + 0.12 * contestability
            + 0.12 * equity_review
            + 0.12 * accountability
            + 0.10 * uncertainty_communication
            - 0.05 * process_burden
            - 0.10 * public_trust_risk
        )

        review_flag = (
            participation < 0.55
            or procedural_fairness < 0.55
            or contestability < 0.55
            or equity_review < 0.55
            or accountability < 0.55
            or public_trust_risk > 0.60
        )

        results.append({
            "process": row["process"],
            "evidence_quality": evidence_quality,
            "transparency": transparency,
            "participation": participation,
            "procedural_fairness": procedural_fairness,
            "contestability": contestability,
            "equity_review": equity_review,
            "accountability": accountability,
            "uncertainty_communication": uncertainty_communication,
            "process_burden": process_burden,
            "public_trust_risk": public_trust_risk,
            "democratic_decision_quality": round(democratic_decision_quality, 6),
            "review_flag": "review" if review_flag else "acceptable",
        })

    results.sort(key=lambda item: float(item["democratic_decision_quality"]), reverse=True)
    for rank, row in enumerate(results, start=1):
        row["rank"] = rank

    write_csv(TABLES / "democratic_public_reasoning_results.csv", results)
    print(TABLES / "democratic_public_reasoning_results.csv")


if __name__ == "__main__":
    main()
