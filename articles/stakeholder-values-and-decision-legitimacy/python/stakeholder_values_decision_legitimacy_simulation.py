#!/usr/bin/env python3
"""
Stakeholder Values and Decision Legitimacy workflow.

Computes stakeholder-specific value scores, aggregate stakeholder scores,
burden exposure, procedural legitimacy, threshold pass rates, decision
legitimacy index, review flags, and decision-record export.

Uses only the Python standard library.
"""

from __future__ import annotations

from pathlib import Path
import csv
import json
from statistics import mean

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
DATA = ARTICLE_ROOT / "data"
TABLES = ARTICLE_ROOT / "outputs" / "tables"
RECORDS = ARTICLE_ROOT / "outputs" / "decision_records"


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def load_criteria() -> list[str]:
    return [row["criterion"] for row in read_csv_dicts(DATA / "synthetic_criteria.csv")]


def load_alternatives() -> list[dict[str, object]]:
    criteria = load_criteria()
    rows = read_csv_dicts(DATA / "synthetic_alternatives.csv")
    output: list[dict[str, object]] = []
    for row in rows:
        item: dict[str, object] = {"alternative": row["alternative"]}
        for criterion in criteria:
            item[criterion] = float(row[criterion])
        output.append(item)
    return output


def load_stakeholders() -> dict[str, dict[str, float]]:
    output: dict[str, dict[str, float]] = {}
    for row in read_csv_dicts(DATA / "synthetic_stakeholders.csv"):
        output[row["stakeholder"]] = {
            "importance": float(row["importance"]),
            "minimum_threshold": float(row["minimum_threshold"]),
        }
    return output


def load_value_weights() -> dict[str, dict[str, float]]:
    output: dict[str, dict[str, float]] = {}
    for row in read_csv_dicts(DATA / "synthetic_value_weights.csv"):
        output.setdefault(row["stakeholder"], {})[row["criterion"]] = float(row["weight"])
    for stakeholder, weights in output.items():
        total = sum(weights.values())
        if abs(total - 1.0) > 1e-9:
            raise ValueError(f"Weights for {stakeholder} must sum to 1. Got {total}.")
    return output


def load_burdens() -> dict[str, dict[str, float]]:
    output: dict[str, dict[str, float]] = {}
    for row in read_csv_dicts(DATA / "synthetic_burdens.csv"):
        output.setdefault(row["alternative"], {})[row["stakeholder"]] = float(row["burden"])
    return output


def load_procedure_scores() -> dict[str, dict[str, float]]:
    output: dict[str, dict[str, float]] = {}
    for row in read_csv_dicts(DATA / "synthetic_procedure_scores.csv"):
        output[row["alternative"]] = {
            "voice": float(row["voice"]),
            "transparency": float(row["transparency"]),
            "explanation": float(row["explanation"]),
            "contestability": float(row["contestability"]),
            "review": float(row["review"]),
        }
    return output


def load_procedure_weights() -> dict[str, float]:
    weights = {
        row["criterion"]: float(row["weight"])
        for row in read_csv_dicts(DATA / "synthetic_procedure_weights.csv")
    }
    total = sum(weights.values())
    if abs(total - 1.0) > 1e-9:
        raise ValueError(f"Procedure weights must sum to 1. Got {total}.")
    return weights


def stakeholder_score(
    alternative: dict[str, object],
    stakeholder: str,
    criteria: list[str],
    value_weights: dict[str, dict[str, float]],
) -> float:
    weights = value_weights[stakeholder]
    return sum(float(alternative[criterion]) * weights[criterion] for criterion in criteria)


def procedural_score(
    alternative_name: str,
    procedure_scores: dict[str, dict[str, float]],
    procedure_weights: dict[str, float],
) -> float:
    values = procedure_scores[alternative_name]
    return sum(values[key] * procedure_weights[key] for key in procedure_weights)


def compute_results() -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    criteria = load_criteria()
    alternatives = load_alternatives()
    stakeholders = load_stakeholders()
    value_weights = load_value_weights()
    burdens = load_burdens()
    procedure_scores = load_procedure_scores()
    procedure_weights = load_procedure_weights()

    stakeholder_rows: list[dict[str, object]] = []
    burden_rows: list[dict[str, object]] = []
    procedure_rows: list[dict[str, object]] = []
    result_rows: list[dict[str, object]] = []

    for alternative in alternatives:
        alternative_name = str(alternative["alternative"])
        aggregate_score = 0.0
        scores_for_thresholds: list[float] = []
        pass_count = 0

        for stakeholder, info in stakeholders.items():
            score = stakeholder_score(alternative, stakeholder, criteria, value_weights)
            threshold = info["minimum_threshold"]
            passes = score >= threshold
            if passes:
                pass_count += 1

            aggregate_score += score * info["importance"]
            scores_for_thresholds.append(score)

            stakeholder_rows.append({
                "alternative": alternative_name,
                "stakeholder": stakeholder,
                "stakeholder_score": round(score, 6),
                "importance": info["importance"],
                "minimum_threshold": threshold,
                "passes_threshold": passes,
            })

        for stakeholder, burden in burdens[alternative_name].items():
            burden_rows.append({
                "alternative": alternative_name,
                "stakeholder": stakeholder,
                "burden": burden,
            })

        proc_score = procedural_score(alternative_name, procedure_scores, procedure_weights)
        proc_record = {"alternative": alternative_name, **procedure_scores[alternative_name], "procedural_score": round(proc_score, 6)}
        procedure_rows.append(proc_record)

        max_burden = max(burdens[alternative_name].values())
        avg_burden = mean(burdens[alternative_name].values())
        pass_rate = pass_count / len(stakeholders)
        min_score = min(scores_for_thresholds)

        decision_legitimacy_index = (
            0.40 * aggregate_score
            + 0.24 * proc_score
            + 0.18 * pass_rate
            + 0.10 * min_score
            - 0.08 * max_burden
        )

        review = pass_rate < 0.80 or max_burden > 0.50 or proc_score < 0.65

        result_rows.append({
            "alternative": alternative_name,
            "aggregate_stakeholder_score": round(aggregate_score, 6),
            "stakeholder_threshold_pass_rate": round(pass_rate, 6),
            "minimum_stakeholder_score": round(min_score, 6),
            "maximum_stakeholder_burden": round(max_burden, 6),
            "average_stakeholder_burden": round(avg_burden, 6),
            "procedural_score": round(proc_score, 6),
            "decision_legitimacy_index": round(decision_legitimacy_index, 6),
            "review_flag": "review" if review else "acceptable",
        })

    ranked = sorted(result_rows, key=lambda row: float(row["decision_legitimacy_index"]), reverse=True)
    for rank, row in enumerate(ranked, start=1):
        row["rank"] = rank

    return stakeholder_rows, burden_rows, procedure_rows, ranked


def weight_rows() -> list[dict[str, object]]:
    weights = load_value_weights()
    return [
        {"stakeholder": stakeholder, "criterion": criterion, "weight": weight}
        for stakeholder, group_weights in weights.items()
        for criterion, weight in group_weights.items()
    ]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"No rows to write: {path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> None:
    stakeholder_rows, burden_rows, procedure_rows, results = compute_results()
    criteria = load_criteria()
    stakeholders = load_stakeholders()
    procedure_weights = load_procedure_weights()

    write_csv(TABLES / "stakeholder_alternative_scores.csv", load_alternatives())
    write_csv(TABLES / "stakeholder_value_weights.csv", weight_rows())
    write_csv(TABLES / "stakeholder_scores_by_group.csv", stakeholder_rows)
    write_csv(TABLES / "stakeholder_burden_table.csv", burden_rows)
    write_csv(TABLES / "procedural_legitimacy_scores.csv", procedure_rows)
    write_csv(TABLES / "decision_legitimacy_results.csv", results)

    write_json(
        RECORDS / "stakeholder_values_decision_record.json",
        {
            "article": "Stakeholder Values and Decision Legitimacy",
            "decision_context": "Comparing alternatives across stakeholder value profiles, burdens, procedural legitimacy, thresholds, and decision-legitimacy diagnostics.",
            "criteria": criteria,
            "stakeholder_importance": stakeholders,
            "procedure_weights": procedure_weights,
            "ranked_results": results,
            "selected_alternative": results[0]["alternative"],
            "review_flags": [row for row in results if row["review_flag"] == "review"],
            "modeling_principles": [
                "Stakeholder values should shape criteria, thresholds, and trade-off review.",
                "Aggregate scores can hide concentrated stakeholder burdens.",
                "Procedural legitimacy requires voice, transparency, explanation, contestability, and review.",
                "Threshold checks prevent low stakeholder performance from being averaged away.",
                "Decision records should preserve stakeholder claims, dissent, burdens, rationale, and review triggers."
            ],
        },
    )

    print("Stakeholder values and decision legitimacy workflow complete.")
    print(TABLES / "decision_legitimacy_results.csv")
    print(RECORDS / "stakeholder_values_decision_record.json")


if __name__ == "__main__":
    main()
