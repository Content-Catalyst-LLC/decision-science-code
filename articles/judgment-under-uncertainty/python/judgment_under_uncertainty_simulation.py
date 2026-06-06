#!/usr/bin/env python3
"""
Judgment Under Uncertainty Simulation

Simulates Bayesian-style updating, anchoring distortion, evidence-quality
effects, forecast confidence, Brier scoring, calibration, review queues,
and decision-record export.

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
class JudgmentCase:
    case_id: int
    domain: str
    prior: float
    likelihood_if_true: float
    likelihood_if_false: float
    anchor: float
    anchor_weight: float
    evidence_quality: str


def clamp(value: float, low: float = 0.01, high: float = 0.99) -> float:
    return max(low, min(high, value))


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def load_seed_cases() -> list[JudgmentCase]:
    rows = read_csv_dicts(DATA / "synthetic_judgment_cases.csv")
    return [
        JudgmentCase(
            case_id=int(row["case_id"]),
            domain=row["domain"],
            prior=float(row["prior"]),
            likelihood_if_true=float(row["likelihood_if_true"]),
            likelihood_if_false=float(row["likelihood_if_false"]),
            anchor=float(row["anchor"]),
            anchor_weight=float(row["anchor_weight"]),
            evidence_quality=row["evidence_quality"],
        )
        for row in rows
    ]


def posterior_from_likelihoods(prior: float, likelihood_if_true: float, likelihood_if_false: float) -> float:
    prior = clamp(prior)
    odds = prior / (1.0 - prior)
    likelihood_ratio = likelihood_if_true / likelihood_if_false
    posterior_odds = odds * likelihood_ratio
    return posterior_odds / (1.0 + posterior_odds)


def brier_score(probability: float, outcome: int) -> float:
    return (probability - outcome) ** 2


def probability_bin(probability: float) -> str:
    lower = int(probability * 10) / 10
    upper = min(1.0, lower + 0.1)
    right = "]" if upper >= 1.0 else ")"
    return f"[{lower:.1f},{upper:.1f}{right}"


def generate_cases(n: int = 900, seed: int = 42) -> list[JudgmentCase]:
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
    quality_weights = [0.25, 0.50, 0.25]
    cases = load_seed_cases()

    for case_id in range(len(cases) + 1, n + 1):
        cases.append(
            JudgmentCase(
                case_id=case_id,
                domain=rng.choice(domains),
                prior=rng.uniform(0.08, 0.85),
                likelihood_if_true=rng.uniform(0.45, 0.95),
                likelihood_if_false=rng.uniform(0.05, 0.60),
                anchor=rng.uniform(0.10, 0.90),
                anchor_weight=rng.uniform(0.15, 0.55),
                evidence_quality=rng.choices(qualities, weights=quality_weights, k=1)[0],
            )
        )

    return cases


def evaluate_case(case: JudgmentCase, rng: random.Random) -> dict[str, object]:
    posterior = posterior_from_likelihoods(
        case.prior,
        case.likelihood_if_true,
        case.likelihood_if_false,
    )

    anchor_adjusted_judgment = clamp(
        case.anchor_weight * case.anchor + (1.0 - case.anchor_weight) * posterior
    )

    if case.evidence_quality == "high":
        noise_sigma = 0.03
    elif case.evidence_quality == "medium":
        noise_sigma = 0.07
    else:
        noise_sigma = 0.12

    forecast_probability = clamp(anchor_adjusted_judgment + rng.gauss(0.0, noise_sigma))
    confidence = clamp(forecast_probability + rng.gauss(0.0, 0.08))
    outcome = 1 if rng.random() < posterior else 0

    score = brier_score(forecast_probability, outcome)
    absolute_error = abs(forecast_probability - outcome)
    confidence_gap = confidence - forecast_probability
    anchor_distortion = abs(anchor_adjusted_judgment - posterior)

    if confidence_gap > 0.10:
        confidence_flag = "overconfident"
    elif confidence_gap < -0.10:
        confidence_flag = "underconfident"
    else:
        confidence_flag = "approximately calibrated"

    review = score > 0.25 or abs(confidence_gap) > 0.15 or anchor_distortion > 0.15

    return {
        "case_id": case.case_id,
        "domain": case.domain,
        "prior": round(case.prior, 6),
        "likelihood_if_true": round(case.likelihood_if_true, 6),
        "likelihood_if_false": round(case.likelihood_if_false, 6),
        "likelihood_ratio": round(case.likelihood_if_true / case.likelihood_if_false, 6),
        "posterior": round(posterior, 6),
        "anchor": round(case.anchor, 6),
        "anchor_weight": round(case.anchor_weight, 6),
        "anchor_adjusted_judgment": round(anchor_adjusted_judgment, 6),
        "forecast_probability": round(forecast_probability, 6),
        "confidence": round(confidence, 6),
        "outcome": outcome,
        "brier_score": round(score, 6),
        "absolute_error": round(absolute_error, 6),
        "confidence_gap": round(confidence_gap, 6),
        "anchor_distortion": round(anchor_distortion, 6),
        "evidence_quality": case.evidence_quality,
        "probability_bin": probability_bin(forecast_probability),
        "confidence_flag": confidence_flag,
        "review_flag": "review" if review else "acceptable",
    }


def group_summary(rows: list[dict[str, object]], field: str) -> list[dict[str, object]]:
    output: list[dict[str, object]] = []

    for group in sorted({str(row[field]) for row in rows}):
        subset = [row for row in rows if row[field] == group]
        output.append({
            field: group,
            "n_cases": len(subset),
            "average_prior": round(mean(float(row["prior"]) for row in subset), 6),
            "average_posterior": round(mean(float(row["posterior"]) for row in subset), 6),
            "average_forecast_probability": round(mean(float(row["forecast_probability"]) for row in subset), 6),
            "observed_frequency": round(mean(int(row["outcome"]) for row in subset), 6),
            "average_brier_score": round(mean(float(row["brier_score"]) for row in subset), 6),
            "average_absolute_error": round(mean(float(row["absolute_error"]) for row in subset), 6),
            "average_confidence_gap": round(mean(float(row["confidence_gap"]) for row in subset), 6),
            "average_anchor_distortion": round(mean(float(row["anchor_distortion"]) for row in subset), 6),
            "review_rate": round(sum(1 for row in subset if row["review_flag"] == "review") / len(subset), 6),
        })

    return output


def calibration_table(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    output: list[dict[str, object]] = []
    n_total = len(rows)

    for bin_name in sorted({str(row["probability_bin"]) for row in rows}):
        subset = [row for row in rows if row["probability_bin"] == bin_name]
        average_forecast = mean(float(row["forecast_probability"]) for row in subset)
        observed_frequency = mean(int(row["outcome"]) for row in subset)
        absolute_gap = abs(average_forecast - observed_frequency)

        output.append({
            "probability_bin": bin_name,
            "n_cases": len(subset),
            "average_forecast_probability": round(average_forecast, 6),
            "observed_frequency": round(observed_frequency, 6),
            "calibration_gap": round(average_forecast - observed_frequency, 6),
            "absolute_calibration_gap": round(absolute_gap, 6),
            "weighted_calibration_error": round((len(subset) / n_total) * absolute_gap, 6),
            "average_brier_score": round(mean(float(row["brier_score"]) for row in subset), 6),
        })

    return output


def overall_metrics(rows: list[dict[str, object]], calibration_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {"metric": "mean_brier_score", "value": round(mean(float(row["brier_score"]) for row in rows), 6)},
        {"metric": "expected_calibration_error", "value": round(sum(float(row["weighted_calibration_error"]) for row in calibration_rows), 6)},
        {"metric": "mean_absolute_error", "value": round(mean(float(row["absolute_error"]) for row in rows), 6)},
        {"metric": "mean_confidence_gap", "value": round(mean(float(row["confidence_gap"]) for row in rows), 6)},
        {"metric": "mean_anchor_distortion", "value": round(mean(float(row["anchor_distortion"]) for row in rows), 6)},
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
    evidence_quality_rows = group_summary(rows, "evidence_quality")
    confidence_rows = group_summary(rows, "confidence_flag")
    calibration_rows = calibration_table(rows)
    metric_rows = overall_metrics(rows, calibration_rows)
    review_rows = [row for row in rows if row["review_flag"] == "review"]

    write_csv(TABLES / "judgment_under_uncertainty_cases.csv", rows)
    write_csv(TABLES / "domain_judgment_quality_summary.csv", domain_rows)
    write_csv(TABLES / "evidence_quality_summary.csv", evidence_quality_rows)
    write_csv(TABLES / "confidence_error_summary.csv", confidence_rows)
    write_csv(TABLES / "judgment_calibration_table.csv", calibration_rows)
    write_csv(TABLES / "judgment_review_queue.csv", review_rows)
    write_csv(TABLES / "overall_judgment_under_uncertainty_metrics.csv", metric_rows)

    write_json(
        RECORDS / "judgment_under_uncertainty_decision_record.json",
        {
            "article": "Judgment Under Uncertainty",
            "decision_context": "Evaluating belief updating, forecast confidence, anchoring distortion, calibration, and cases requiring judgment review.",
            "modeling_principles": [
                "Judgment under uncertainty should distinguish prior belief, evidence, posterior belief, forecast probability, and confidence.",
                "Base rates and likelihoods should discipline case-specific interpretation.",
                "Confidence should be scored against outcomes over repeated judgments.",
                "Anchoring, overconfidence, and evidence-quality issues should trigger review.",
                "Decision records should preserve assumptions, evidence, confidence, and revision logic before outcomes are known.",
            ],
            "overall_metrics": metric_rows,
            "domain_summary": domain_rows,
            "evidence_quality_summary": evidence_quality_rows,
            "confidence_summary": confidence_rows,
            "calibration_summary": calibration_rows,
            "review_queue_size": len(review_rows),
        },
    )

    print("Judgment under uncertainty workflow complete.")
    print(TABLES / "judgment_under_uncertainty_cases.csv")
    print(TABLES / "domain_judgment_quality_summary.csv")
    print(TABLES / "judgment_calibration_table.csv")
    print(TABLES / "judgment_review_queue.csv")
    print(RECORDS / "judgment_under_uncertainty_decision_record.json")


if __name__ == "__main__":
    main()
