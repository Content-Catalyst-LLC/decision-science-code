#!/usr/bin/env python3
"""
Multi-Criteria Decision Analysis workflow.

Simulates MCDA ranking under base weights and uncertain weights.
Exports normalized scores, base results, rank stability, criterion
contributions, review flags, and decision records.

Uses only the Python standard library.
"""

from __future__ import annotations

from pathlib import Path
import csv
import json
import random
from statistics import mean, stdev

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
DATA = ARTICLE_ROOT / "data"
TABLES = ARTICLE_ROOT / "outputs" / "tables"
RECORDS = ARTICLE_ROOT / "outputs" / "decision_records"

CRITERIA = [
    "cost",
    "implementation_feasibility",
    "equity",
    "resilience",
    "environmental_benefit",
    "long_term_value",
    "legitimacy",
]

DIRECTION = {
    "cost": "cost",
    "implementation_feasibility": "benefit",
    "equity": "benefit",
    "resilience": "benefit",
    "environmental_benefit": "benefit",
    "long_term_value": "benefit",
    "legitimacy": "benefit",
}

BASE_WEIGHTS = {
    "cost": 0.16,
    "implementation_feasibility": 0.14,
    "equity": 0.16,
    "resilience": 0.17,
    "environmental_benefit": 0.13,
    "long_term_value": 0.15,
    "legitimacy": 0.09,
}


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def ensure_weights(weights: dict[str, float]) -> None:
    total = sum(weights.values())
    if abs(total - 1.0) > 1e-9:
        raise ValueError(f"Weights must sum to 1. Got {total}.")


def load_alternatives() -> list[dict[str, object]]:
    rows = read_csv_dicts(DATA / "synthetic_alternatives.csv")
    output: list[dict[str, object]] = []
    for row in rows:
        converted: dict[str, object] = {"alternative": row["alternative"]}
        for criterion in CRITERIA:
            converted[criterion] = float(row[criterion])
        output.append(converted)
    return output


def normalize_values(values: list[float], direction: str) -> list[float]:
    low = min(values)
    high = max(values)
    if high == low:
        return [1.0 for _ in values]

    if direction == "benefit":
        return [(value - low) / (high - low) for value in values]

    if direction == "cost":
        return [(high - value) / (high - low) for value in values]

    raise ValueError("Direction must be 'benefit' or 'cost'.")


def normalize_alternatives(alternatives: list[dict[str, object]]) -> list[dict[str, object]]:
    normalized: list[dict[str, object]] = [{"alternative": row["alternative"]} for row in alternatives]

    for criterion in CRITERIA:
        values = [float(row[criterion]) for row in alternatives]
        normalized_values = normalize_values(values, DIRECTION[criterion])

        for index, value in enumerate(normalized_values):
            normalized[index][criterion] = round(value, 6)

    return normalized


def weighted_score(row: dict[str, object], weights: dict[str, float]) -> float:
    return sum(float(row[criterion]) * weights[criterion] for criterion in CRITERIA)


def rank_rows(rows: list[dict[str, object]], score_field: str = "composite_score") -> list[dict[str, object]]:
    sorted_rows = sorted(rows, key=lambda row: float(row[score_field]), reverse=True)
    output: list[dict[str, object]] = []

    for rank, row in enumerate(sorted_rows, start=1):
        new_row = dict(row)
        new_row["rank"] = rank
        output.append(new_row)

    return output


def random_weight_vector(rng: random.Random, base_weights: dict[str, float], concentration: float = 80.0) -> dict[str, float]:
    draws = {
        criterion: rng.gammavariate(max(base_weights[criterion] * concentration, 0.001), 1.0)
        for criterion in CRITERIA
    }
    total = sum(draws.values())
    return {criterion: value / total for criterion, value in draws.items()}


def criterion_contributions(normalized: list[dict[str, object]], weights: dict[str, float]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for row in normalized:
        contribution: dict[str, object] = {"alternative": row["alternative"]}
        total = 0.0

        for criterion in CRITERIA:
            value = float(row[criterion]) * weights[criterion]
            contribution[criterion] = round(value, 6)
            total += value

        contribution["total_score"] = round(total, 6)
        rows.append(contribution)
    return rows


def stakeholder_profile_results(normalized: list[dict[str, object]]) -> list[dict[str, object]]:
    profile_rows = read_csv_dicts(DATA / "synthetic_stakeholder_profiles.csv")
    profiles = sorted({row["profile"] for row in profile_rows})
    output: list[dict[str, object]] = []

    for profile in profiles:
        weights = {
            row["criterion"]: float(row["weight"])
            for row in profile_rows
            if row["profile"] == profile
        }
        ensure_weights(weights)

        scored = [
            {
                "profile": profile,
                "alternative": row["alternative"],
                "composite_score": round(weighted_score(row, weights), 6),
            }
            for row in normalized
        ]

        ranked = rank_rows(scored)
        output.extend(ranked)

    return output


def outranking_pairs(normalized: list[dict[str, object]], weights: dict[str, float]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for a in normalized:
        for b in normalized:
            if a["alternative"] == b["alternative"]:
                continue
            concordance = sum(
                weights[criterion]
                for criterion in CRITERIA
                if float(a[criterion]) >= float(b[criterion])
            )
            discordance_count = sum(
                1
                for criterion in CRITERIA
                if float(a[criterion]) + 0.15 < float(b[criterion])
            )
            rows.append({
                "alternative_a": a["alternative"],
                "alternative_b": b["alternative"],
                "concordance": round(concordance, 6),
                "discordance_count": discordance_count,
                "a_outranks_b": concordance >= 0.60 and discordance_count == 0,
            })
    return rows


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
    ensure_weights(BASE_WEIGHTS)
    rng = random.Random(42)

    alternatives = load_alternatives()
    normalized = normalize_alternatives(alternatives)

    scored = [
        {
            "alternative": row["alternative"],
            "composite_score": round(weighted_score(row, BASE_WEIGHTS), 6),
        }
        for row in normalized
    ]

    base_results = rank_rows(scored)

    n_simulations = 3000
    simulation_rows: list[dict[str, object]] = []

    for simulation_id in range(1, n_simulations + 1):
        weights = random_weight_vector(rng, BASE_WEIGHTS)

        sim_scored = [
            {
                "alternative": row["alternative"],
                "score": weighted_score(row, weights),
            }
            for row in normalized
        ]

        sim_ranked = rank_rows(sim_scored, score_field="score")

        for row in sim_ranked:
            simulation_rows.append({
                "simulation_id": simulation_id,
                "alternative": row["alternative"],
                "score": round(float(row["score"]), 6),
                "rank": row["rank"],
            })

    rank_summary: list[dict[str, object]] = []
    alternative_names = [str(row["alternative"]) for row in normalized]

    for alternative in alternative_names:
        subset = [row for row in simulation_rows if row["alternative"] == alternative]
        ranks = [int(row["rank"]) for row in subset]
        scores = [float(row["score"]) for row in subset]

        rank_summary.append({
            "alternative": alternative,
            "average_score": round(mean(scores), 6),
            "min_score": round(min(scores), 6),
            "max_score": round(max(scores), 6),
            "average_rank": round(mean(ranks), 6),
            "best_rank_rate": round(sum(1 for rank in ranks if rank == 1) / len(ranks), 6),
            "top_two_rate": round(sum(1 for rank in ranks if rank <= 2) / len(ranks), 6),
            "rank_volatility": round(stdev(ranks), 6),
        })

    rank_summary = sorted(rank_summary, key=lambda row: (-float(row["best_rank_rate"]), float(row["average_rank"])))

    contribution_rows = criterion_contributions(normalized, BASE_WEIGHTS)
    stakeholder_rows = stakeholder_profile_results(normalized)
    outranking_rows = outranking_pairs(normalized, BASE_WEIGHTS)

    max_score = max(float(row["composite_score"]) for row in base_results)
    rank_summary_by_name = {row["alternative"]: row for row in rank_summary}
    review_rows: list[dict[str, object]] = []

    for row in base_results:
        stability = rank_summary_by_name[row["alternative"]]
        score_gap = max_score - float(row["composite_score"])

        review_flag = (
            float(stability["best_rank_rate"]) < 0.25
            or float(stability["rank_volatility"]) > 1.25
            or score_gap < 0.03
        )

        review_rows.append({
            "alternative": row["alternative"],
            "base_rank": row["rank"],
            "base_score": row["composite_score"],
            "best_rank_rate": stability["best_rank_rate"],
            "top_two_rate": stability["top_two_rate"],
            "rank_volatility": stability["rank_volatility"],
            "score_gap_from_leader": round(score_gap, 6),
            "review_flag": "review" if review_flag else "acceptable",
        })

    weight_rows = [{"criterion": criterion, "weight": BASE_WEIGHTS[criterion]} for criterion in CRITERIA]

    write_csv(TABLES / "mcda_raw_alternative_profiles.csv", alternatives)
    write_csv(TABLES / "mcda_normalized_alternative_profiles.csv", normalized)
    write_csv(TABLES / "mcda_base_weights.csv", weight_rows)
    write_csv(TABLES / "mcda_base_results.csv", base_results)
    write_csv(TABLES / "mcda_weight_sensitivity_simulations.csv", simulation_rows)
    write_csv(TABLES / "mcda_rank_stability_summary.csv", rank_summary)
    write_csv(TABLES / "mcda_criterion_contributions.csv", contribution_rows)
    write_csv(TABLES / "mcda_stakeholder_profile_results.csv", stakeholder_rows)
    write_csv(TABLES / "mcda_outranking_pairs.csv", outranking_rows)
    write_csv(TABLES / "mcda_review_flags.csv", review_rows)

    write_json(
        RECORDS / "mcda_decision_record.json",
        {
            "article": "Multi-Criteria Decision Analysis",
            "decision_context": "Comparing alternatives across cost, feasibility, equity, resilience, environmental benefit, long-term value, and legitimacy.",
            "criteria": CRITERIA,
            "directions": DIRECTION,
            "base_weights": BASE_WEIGHTS,
            "base_results": base_results,
            "rank_stability": rank_summary,
            "stakeholder_profile_results": stakeholder_rows,
            "review_flags": review_rows,
            "modeling_principles": [
                "MCDA rankings depend on criteria, scores, weights, normalization, and aggregation logic.",
                "Weights encode value judgments and should be documented.",
                "Sensitivity analysis is necessary before interpreting rankings.",
                "Rank stability can be more informative than a single preferred alternative.",
                "MCDA should support deliberation, not replace accountable judgment.",
            ],
        },
    )

    print("MCDA workflow complete.")
    print(TABLES / "mcda_base_results.csv")
    print(TABLES / "mcda_rank_stability_summary.csv")
    print(TABLES / "mcda_review_flags.csv")
    print(RECORDS / "mcda_decision_record.json")


if __name__ == "__main__":
    main()
