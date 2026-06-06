#!/usr/bin/env python3
"""
Overconfidence and Decision Failure Simulation

Simulates confidence error, probabilistic forecast calibration, Brier scoring,
planning bias, interval coverage, review queues, and decision-record export.

Uses only the Python standard library.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import csv
import json
import random
from statistics import mean

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
DATA = ARTICLE_ROOT / "data"
TABLES = ARTICLE_ROOT / "outputs" / "tables"
RECORDS = ARTICLE_ROOT / "outputs" / "decision_records"


@dataclass(frozen=True)
class DecisionCase:
    case_id: int
    domain: str
    forecast_probability: float
    confidence: float
    evidence_quality: str
    estimated_duration: float
    estimated_cost: float
    interval_width_factor: float


def clamp(value: float, low: float = 0.01, high: float = 0.99) -> float:
    return max(low, min(high, value))


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def brier_score(probability: float, outcome: int) -> float:
    return (probability - outcome) ** 2


def probability_bin(probability: float) -> str:
    lower = int(probability * 10) / 10
    upper = min(1.0, lower + 0.1)
    right = "]" if upper >= 1.0 else ")"
    return f"[{lower:.1f},{upper:.1f}{right}"


def load_seed_cases() -> list[DecisionCase]:
    forecasts = read_csv_dicts(DATA / "synthetic_forecasts.csv")
    planning = read_csv_dicts(DATA / "synthetic_planning_estimates.csv")
    planning_by_id = {int(row["case_id"]): row for row in planning}
    cases: list[DecisionCase] = []

    for index, row in enumerate(forecasts, start=1):
        plan = planning_by_id.get(index)
        cases.append(
            DecisionCase(
                case_id=index,
                domain=row["domain"],
                forecast_probability=float(row["forecast_probability"]),
                confidence=float(row["confidence"]),
                evidence_quality=row["evidence_quality"],
                estimated_duration=float(plan["estimated_duration"]) if plan else 120.0,
                estimated_cost=float(plan["estimated_cost"]) if plan else 500000.0,
                interval_width_factor=0.20,
            )
        )

    return cases


def generate_cases(n: int = 900, seed: int = 42) -> list[DecisionCase]:
    rng = random.Random(seed)
    domains = [
        "Public Policy",
        "Healthcare",
        "Financial Risk",
        "Infrastructure",
        "AI Governance",
        "Organizational Strategy",
    ]
    qualities = ["low", "medium", "high"]
    weights = [0.25, 0.50, 0.25]

    cases = load_seed_cases()

    for case_id in range(len(cases) + 1, n + 1):
        cases.append(
            DecisionCase(
                case_id=case_id,
                domain=rng.choice(domains),
                forecast_probability=rng.uniform(0.10, 0.95),
                confidence=rng.uniform(0.50, 0.99),
                evidence_quality=rng.choices(qualities, weights=weights, k=1)[0],
                estimated_duration=rng.uniform(30.0, 365.0),
                estimated_cost=rng.uniform(100_000.0, 5_000_000.0),
                interval_width_factor=rng.uniform(0.05, 0.30),
            )
        )

    return cases


def quality_noise(evidence_quality: str) -> float:
    if evidence_quality == "high":
        return 0.03
    if evidence_quality == "medium":
        return 0.08
    if evidence_quality == "low":
        return 0.15
    raise ValueError("Evidence quality must be low, medium, or high.")


def evaluate_case(case: DecisionCase, rng: random.Random) -> dict[str, object]:
    true_probability = clamp(
        case.forecast_probability - rng.uniform(0.00, 0.18) + rng.gauss(0.0, quality_noise(case.evidence_quality))
    )

    outcome = 1 if rng.random() < true_probability else 0
    score = brier_score(case.forecast_probability, outcome)
    accuracy_proxy = 1.0 - score
    confidence_error = case.confidence - accuracy_proxy

    duration_bias = rng.lognormvariate(0.182, 0.30)
    cost_bias = rng.lognormvariate(0.165, 0.35)

    actual_duration = case.estimated_duration * duration_bias
    actual_cost = case.estimated_cost * cost_bias

    duration_error = (actual_duration - case.estimated_duration) / case.estimated_duration
    cost_error = (actual_cost - case.estimated_cost) / case.estimated_cost

    duration_lower = case.estimated_duration * (1.0 - case.interval_width_factor)
    duration_upper = case.estimated_duration * (1.0 + case.interval_width_factor)
    cost_lower = case.estimated_cost * (1.0 - case.interval_width_factor)
    cost_upper = case.estimated_cost * (1.0 + case.interval_width_factor)

    duration_interval_hit = duration_lower <= actual_duration <= duration_upper
    cost_interval_hit = cost_lower <= actual_cost <= cost_upper

    if confidence_error > 0.15:
        confidence_flag = "overconfident"
    elif confidence_error < -0.15:
        confidence_flag = "underconfident"
    else:
        confidence_flag = "approximately calibrated"

    review = (
        confidence_error > 0.15
        or score > 0.25
        or duration_error > 0.30
        or cost_error > 0.30
        or not duration_interval_hit
        or not cost_interval_hit
    )

    return {
        "case_id": case.case_id,
        "domain": case.domain,
        "forecast_probability": round(case.forecast_probability, 6),
        "true_probability": round(true_probability, 6),
        "confidence": round(case.confidence, 6),
        "evidence_quality": case.evidence_quality,
        "outcome": outcome,
        "brier_score": round(score, 6),
        "accuracy_proxy": round(accuracy_proxy, 6),
        "confidence_error": round(confidence_error, 6),
        "confidence_flag": confidence_flag,
        "estimated_duration": round(case.estimated_duration, 6),
        "actual_duration": round(actual_duration, 6),
        "duration_planning_error": round(duration_error, 6),
        "estimated_cost": round(case.estimated_cost, 6),
        "actual_cost": round(actual_cost, 6),
        "cost_planning_error": round(cost_error, 6),
        "interval_width_factor": round(case.interval_width_factor, 6),
        "duration_interval_hit": duration_interval_hit,
        "cost_interval_hit": cost_interval_hit,
        "probability_bin": probability_bin(case.forecast_probability),
        "review_flag": "review" if review else "acceptable",
    }


def group_summary(rows: list[dict[str, object]], field: str) -> list[dict[str, object]]:
    output: list[dict[str, object]] = []

    for group in sorted({str(row[field]) for row in rows}):
        subset = [row for row in rows if row[field] == group]
        output.append({
            field: group,
            "n_cases": len(subset),
            "average_forecast_probability": round(mean(float(row["forecast_probability"]) for row in subset), 6),
            "observed_frequency": round(mean(int(row["outcome"]) for row in subset), 6),
            "average_confidence": round(mean(float(row["confidence"]) for row in subset), 6),
            "average_brier_score": round(mean(float(row["brier_score"]) for row in subset), 6),
            "average_confidence_error": round(mean(float(row["confidence_error"]) for row in subset), 6),
            "duration_interval_coverage": round(sum(1 for row in subset if row["duration_interval_hit"]) / len(subset), 6),
            "cost_interval_coverage": round(sum(1 for row in subset if row["cost_interval_hit"]) / len(subset), 6),
            "average_duration_planning_error": round(mean(float(row["duration_planning_error"]) for row in subset), 6),
            "average_cost_planning_error": round(mean(float(row["cost_planning_error"]) for row in subset), 6),
            "review_rate": round(sum(1 for row in subset if row["review_flag"] == "review") / len(subset), 6),
        })

    return output


def calibration_table(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    output: list[dict[str, object]] = []
    n_total = len(rows)

    for bin_name in sorted({str(row["probability_bin"]) for row in rows}):
        subset = [row for row in rows if row["probability_bin"] == bin_name]
        avg_forecast = mean(float(row["forecast_probability"]) for row in subset)
        observed = mean(int(row["outcome"]) for row in subset)
        abs_gap = abs(avg_forecast - observed)

        output.append({
            "probability_bin": bin_name,
            "n_cases": len(subset),
            "average_forecast_probability": round(avg_forecast, 6),
            "observed_frequency": round(observed, 6),
            "calibration_gap": round(avg_forecast - observed, 6),
            "absolute_calibration_gap": round(abs_gap, 6),
            "weighted_calibration_error": round((len(subset) / n_total) * abs_gap, 6),
            "average_brier_score": round(mean(float(row["brier_score"]) for row in subset), 6),
            "average_confidence": round(mean(float(row["confidence"]) for row in subset), 6),
        })

    return output


def overall_metrics(rows: list[dict[str, object]], calibration_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {"metric": "mean_brier_score", "value": round(mean(float(row["brier_score"]) for row in rows), 6)},
        {"metric": "expected_calibration_error", "value": round(sum(float(row["weighted_calibration_error"]) for row in calibration_rows), 6)},
        {"metric": "mean_confidence_error", "value": round(mean(float(row["confidence_error"]) for row in rows), 6)},
        {"metric": "duration_interval_coverage", "value": round(sum(1 for row in rows if row["duration_interval_hit"]) / len(rows), 6)},
        {"metric": "cost_interval_coverage", "value": round(sum(1 for row in rows if row["cost_interval_hit"]) / len(rows), 6)},
        {"metric": "mean_duration_planning_error", "value": round(mean(float(row["duration_planning_error"]) for row in rows), 6)},
        {"metric": "mean_cost_planning_error", "value": round(mean(float(row["cost_planning_error"]) for row in rows), 6)},
        {"metric": "review_rate", "value": round(sum(1 for row in rows if row["review_flag"] == "review") / len(rows), 6)},
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
    rng = random.Random(123)
    cases = generate_cases(n=900, seed=42)
    rows = [evaluate_case(case, rng) for case in cases]

    domain_rows = group_summary(rows, "domain")
    evidence_rows = group_summary(rows, "evidence_quality")
    confidence_rows = group_summary(rows, "confidence_flag")
    calibration_rows = calibration_table(rows)
    metrics = overall_metrics(rows, calibration_rows)
    review_rows = [row for row in rows if row["review_flag"] == "review"]

    write_csv(TABLES / "overconfidence_decision_cases.csv", rows)
    write_csv(TABLES / "domain_overconfidence_summary.csv", domain_rows)
    write_csv(TABLES / "evidence_quality_overconfidence_summary.csv", evidence_rows)
    write_csv(TABLES / "confidence_error_summary.csv", confidence_rows)
    write_csv(TABLES / "overconfidence_calibration_table.csv", calibration_rows)
    write_csv(TABLES / "overconfidence_review_queue.csv", review_rows)
    write_csv(TABLES / "overall_overconfidence_metrics.csv", metrics)

    write_json(
        RECORDS / "overconfidence_decision_record.json",
        {
            "article": "Overconfidence and Decision Failure",
            "decision_context": "Evaluating confidence error, forecast calibration, interval coverage, planning bias, and review triggers.",
            "modeling_principles": [
                "Confidence should be compared with accuracy and evidence quality.",
                "Forecast probabilities should be scored against outcomes.",
                "Intervals should be checked for coverage to detect overprecision.",
                "Planning estimates should be compared with actual cost and duration.",
                "Decision records should preserve confidence, uncertainty ranges, assumptions, dissent, and review triggers before outcomes are known.",
            ],
            "overall_metrics": metrics,
            "domain_summary": domain_rows,
            "evidence_quality_summary": evidence_rows,
            "confidence_summary": confidence_rows,
            "calibration_summary": calibration_rows,
            "review_queue_size": len(review_rows),
        },
    )

    print("Overconfidence decision failure workflow complete.")
    print(TABLES / "overconfidence_decision_cases.csv")
    print(TABLES / "domain_overconfidence_summary.csv")
    print(TABLES / "overconfidence_calibration_table.csv")
    print(TABLES / "overconfidence_review_queue.csv")
    print(RECORDS / "overconfidence_decision_record.json")


if __name__ == "__main__":
    main()
