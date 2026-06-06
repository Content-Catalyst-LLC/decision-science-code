#!/usr/bin/env python3
"""
Decision Quality and Strategic Alignment workflow.

Simulates process quality, strategic fit, implementation readiness,
adaptive performance, alignment drift, review flags, and decision-record export.

Uses only the Python standard library.
"""

from __future__ import annotations

from pathlib import Path
import csv
import json
import math
import random
from statistics import mean, stdev

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
DATA = ARTICLE_ROOT / "data"
TABLES = ARTICLE_ROOT / "outputs" / "tables"
RECORDS = ARTICLE_ROOT / "outputs" / "decision_records"

QUALITY_DIMENSIONS = [
    "objective_clarity",
    "alternative_quality",
    "information_strength",
    "tradeoff_transparency",
    "uncertainty_treatment",
    "implementation_readiness",
]

ALIGNMENT_DIMENSIONS = [
    "strategic_fit",
    "capability_fit",
    "value_fit",
]


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def load_decisions() -> list[dict[str, object]]:
    rows = read_csv_dicts(DATA / "synthetic_decisions.csv")
    output: list[dict[str, object]] = []
    for row in rows:
        item: dict[str, object] = {"decision": row["decision"]}
        for key, value in row.items():
            if key != "decision":
                item[key] = float(value)
        output.append(item)
    return output


def load_weight_file(path: Path, key_field: str = "dimension", value_field: str = "weight") -> dict[str, float]:
    weights = {row[key_field]: float(row[value_field]) for row in read_csv_dicts(path)}
    ensure_weights(weights)
    return weights


def ensure_weights(weights: dict[str, float]) -> None:
    total = sum(weights.values())
    if abs(total - 1.0) > 1e-9:
        raise ValueError(f"Weights must sum to 1. Got {total}.")


def weighted_score(row: dict[str, object], dimensions: list[str], weights: dict[str, float]) -> float:
    return sum(float(row[dimension]) * weights[dimension] for dimension in dimensions)


def cosine_similarity(a: dict[str, float], b: dict[str, float]) -> float:
    keys = sorted(a.keys())
    dot = sum(a[key] * b[key] for key in keys)
    norm_a = math.sqrt(sum(a[key] ** 2 for key in keys))
    norm_b = math.sqrt(sum(b[key] ** 2 for key in keys))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def rank_rows(rows: list[dict[str, object]], score_field: str) -> list[dict[str, object]]:
    output: list[dict[str, object]] = []
    for rank, row in enumerate(sorted(rows, key=lambda x: float(x[score_field]), reverse=True), start=1):
        item = dict(row)
        item["rank"] = rank
        output.append(item)
    return output


def simulate_performance(
    base_value: float,
    decision_quality: float,
    strategic_alignment: float,
    implementation_readiness: float,
    cycles: int,
    rng: random.Random,
) -> list[dict[str, object]]:
    value = base_value
    rows: list[dict[str, object]] = []

    for cycle in range(1, cycles + 1):
        shock = rng.gauss(0.0, 1.6)
        quality_effect = decision_quality * rng.uniform(0.4, 1.0)
        alignment_effect = strategic_alignment * rng.uniform(0.5, 1.1)
        execution_effect = implementation_readiness * rng.uniform(0.3, 0.9)
        growth_rate = 0.50 + shock + quality_effect + alignment_effect + execution_effect
        value = max(40.0, value * (1.0 + growth_rate / 100.0))

        rows.append({
            "cycle": cycle,
            "performance_value": round(value, 6),
            "growth_rate": round(growth_rate, 6),
        })

    return rows


def simulate_alignment_drift(strategy_vector: dict[str, float], periods: int, rng: random.Random) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    strategy_keys = sorted(strategy_vector.keys())

    for period in range(1, periods + 1):
        observed: dict[str, float] = {}
        for key in strategy_keys:
            drift_push = 0.025 * period if key == "growth" else -0.007 * period
            value = max(0.01, strategy_vector[key] + rng.gauss(0.0, 0.05) + drift_push)
            observed[key] = value

        total = sum(observed.values())
        observed = {key: value / total for key, value in observed.items()}
        alignment = cosine_similarity(observed, strategy_vector)

        row: dict[str, object] = {
            "period": period,
            "alignment": round(alignment, 6),
            "strategic_drift": round(1.0 - alignment, 6),
        }
        for key in strategy_keys:
            row[key] = round(observed[key], 6)
        rows.append(row)

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
    decisions = load_decisions()
    quality_weights = load_weight_file(DATA / "synthetic_quality_dimensions.csv")
    alignment_weights = load_weight_file(DATA / "synthetic_alignment_dimensions.csv")
    strategy_vector = load_weight_file(DATA / "synthetic_strategy_vectors.csv")
    rng = random.Random(42)

    scored_rows: list[dict[str, object]] = []

    for decision in decisions:
        quality_score = weighted_score(decision, QUALITY_DIMENSIONS, quality_weights)
        alignment_score = weighted_score(decision, ALIGNMENT_DIMENSIONS, alignment_weights)
        strategy_profile = {key: float(decision[key]) for key in strategy_vector}
        strategy_vector_alignment = cosine_similarity(strategy_profile, strategy_vector)
        implementation_readiness = float(decision["implementation_readiness"])

        combined_value = (
            0.45 * quality_score
            + 0.40 * alignment_score
            + 0.15 * implementation_readiness
        )

        scored_rows.append({
            "decision": decision["decision"],
            "decision_quality_score": round(quality_score, 6),
            "strategic_alignment_score": round(alignment_score, 6),
            "strategy_vector_alignment": round(strategy_vector_alignment, 6),
            "implementation_readiness": round(implementation_readiness, 6),
            "combined_decision_value": round(combined_value, 6),
        })

    ranked_rows = rank_rows(scored_rows, "combined_decision_value")

    performance_rows: list[dict[str, object]] = []
    performance_summary: list[dict[str, object]] = []

    for row in ranked_rows:
        series = simulate_performance(
            base_value=100.0,
            decision_quality=float(row["decision_quality_score"]),
            strategic_alignment=float(row["strategic_alignment_score"]),
            implementation_readiness=float(row["implementation_readiness"]),
            cycles=40,
            rng=rng,
        )

        values = [float(item["performance_value"]) for item in series]

        for item in series:
            performance_rows.append({"decision": row["decision"], **item})

        performance_summary.append({
            "decision": row["decision"],
            "final_value": round(values[-1], 6),
            "min_value": round(min(values), 6),
            "max_value": round(max(values), 6),
            "average_value": round(mean(values), 6),
            "volatility": round(stdev(values), 6),
        })

    drift_rows = simulate_alignment_drift(strategy_vector, periods=12, rng=rng)

    review_rows: list[dict[str, object]] = []
    for row in ranked_rows:
        review = (
            float(row["decision_quality_score"]) < 0.70
            or float(row["strategic_alignment_score"]) < 0.70
            or float(row["strategy_vector_alignment"]) < 0.85
            or float(row["implementation_readiness"]) < 0.65
        )
        review_rows.append({
            "decision": row["decision"],
            "rank": row["rank"],
            "decision_quality_score": row["decision_quality_score"],
            "strategic_alignment_score": row["strategic_alignment_score"],
            "strategy_vector_alignment": row["strategy_vector_alignment"],
            "implementation_readiness": row["implementation_readiness"],
            "combined_decision_value": row["combined_decision_value"],
            "review_flag": "review" if review else "acceptable",
        })

    write_csv(TABLES / "decision_quality_alignment_profiles.csv", ranked_rows)
    write_csv(TABLES / "decision_quality_alignment_performance.csv", performance_rows)
    write_csv(TABLES / "decision_quality_alignment_performance_summary.csv", performance_summary)
    write_csv(TABLES / "decision_pattern_alignment_drift.csv", drift_rows)
    write_csv(TABLES / "decision_quality_alignment_review_flags.csv", review_rows)

    write_json(
        RECORDS / "decision_quality_alignment_record.json",
        {
            "article": "Decision Quality and Strategic Alignment",
            "decision_context": "Evaluating decisions by process quality, strategic fit, implementation readiness, adaptive performance, and alignment drift.",
            "quality_dimensions": QUALITY_DIMENSIONS,
            "alignment_dimensions": ALIGNMENT_DIMENSIONS,
            "quality_weights": quality_weights,
            "alignment_weights": alignment_weights,
            "strategy_vector": strategy_vector,
            "ranked_decisions": ranked_rows,
            "performance_summary": performance_summary,
            "alignment_drift": drift_rows,
            "review_flags": review_rows,
            "modeling_principles": [
                "Decision quality should be evaluated separately from outcome quality.",
                "Strategic alignment should be demonstrated through criteria, trade-offs, and resource implications.",
                "High-quality misaligned decisions can produce elegant irrelevance.",
                "Aligned but low-quality decisions can produce coherent failure.",
                "Decision records preserve assumptions, rationale, dissent, strategic fit, and review triggers."
            ],
        },
    )

    print("Decision quality and strategic alignment workflow complete.")
    print(TABLES / "decision_quality_alignment_profiles.csv")
    print(TABLES / "decision_quality_alignment_performance_summary.csv")
    print(TABLES / "decision_pattern_alignment_drift.csv")
    print(TABLES / "decision_quality_alignment_review_flags.csv")
    print(RECORDS / "decision_quality_alignment_record.json")


if __name__ == "__main__":
    main()
