#!/usr/bin/env python3
"""
Decision Hygiene and Bias Reduction Simulation

Simulates judgment before and after decision hygiene practices.
Measures bias, noise, mean squared error, calibration, Brier scores,
error reduction, review queues, and decision-record export.

Uses only the Python standard library.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import csv
import json
import random
from statistics import mean, stdev

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
DATA = ARTICLE_ROOT / "data"
TABLES = ARTICLE_ROOT / "outputs" / "tables"
RECORDS = ARTICLE_ROOT / "outputs" / "decision_records"


@dataclass(frozen=True)
class HygieneCase:
    case_id: int
    domain: str
    bias_source: str
    hygiene_practice: str
    true_value: float
    evidence_quality: str
    decision_stakes: str


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


def load_seed_cases() -> list[HygieneCase]:
    rows = read_csv_dicts(DATA / "synthetic_decision_cases.csv")
    return [
        HygieneCase(
            case_id=int(row["case_id"]),
            domain=row["domain"],
            bias_source=row["bias_source"],
            hygiene_practice=row["hygiene_practice"],
            true_value=float(row["true_value"]),
            evidence_quality=row["evidence_quality"],
            decision_stakes=row["decision_stakes"],
        )
        for row in rows
    ]


def generate_cases(n: int = 900, seed: int = 42) -> list[HygieneCase]:
    rng = random.Random(seed)

    domains = [
        "Public Policy",
        "Healthcare",
        "Financial Risk",
        "Infrastructure",
        "AI Governance",
        "Organizational Strategy",
    ]

    bias_sources = [
        "anchoring",
        "availability",
        "confirmation",
        "overconfidence",
        "framing",
        "groupthink",
        "model_overtrust",
    ]

    hygiene_practices = [
        "independent_estimates",
        "base_rate_check",
        "structured_dissent",
        "premortem",
        "calibration_review",
        "decision_record",
        "model_validation",
    ]

    cases = load_seed_cases()

    for case_id in range(len(cases) + 1, n + 1):
        evidence_quality = rng.choices(["low", "medium", "high"], weights=[0.25, 0.50, 0.25], k=1)[0]
        decision_stakes = rng.choices(["low", "medium", "high"], weights=[0.25, 0.45, 0.30], k=1)[0]

        cases.append(
            HygieneCase(
                case_id=case_id,
                domain=rng.choice(domains),
                bias_source=rng.choice(bias_sources),
                hygiene_practice=rng.choice(hygiene_practices),
                true_value=rng.uniform(0.10, 0.90),
                evidence_quality=evidence_quality,
                decision_stakes=decision_stakes,
            )
        )

    return cases


def noise_level(evidence_quality: str) -> float:
    if evidence_quality == "high":
        return 0.05
    if evidence_quality == "medium":
        return 0.09
    if evidence_quality == "low":
        return 0.14
    raise ValueError("Evidence quality must be low, medium, or high.")


def bias_direction(bias_source: str, rng: random.Random) -> float:
    if bias_source in {"anchoring", "overconfidence", "confirmation", "model_overtrust"}:
        return rng.uniform(0.04, 0.16)
    return rng.uniform(-0.10, 0.10)


def hygiene_effect(hygiene_practice: str, rng: random.Random) -> float:
    if hygiene_practice in {
        "independent_estimates",
        "base_rate_check",
        "structured_dissent",
        "calibration_review",
    }:
        return rng.uniform(0.25, 0.55)
    return rng.uniform(0.15, 0.45)


def evaluate_case(case: HygieneCase, rng: random.Random) -> dict[str, object]:
    source_bias = bias_direction(case.bias_source, rng)
    source_noise = noise_level(case.evidence_quality)
    hygiene_strength = hygiene_effect(case.hygiene_practice, rng)

    pre_judgment = clamp(case.true_value + source_bias + rng.gauss(0.0, source_noise))
    post_judgment = clamp(
        case.true_value
        + source_bias * (1.0 - hygiene_strength)
        + rng.gauss(0.0, source_noise * (1.0 - hygiene_strength / 2.0))
    )

    outcome = 1 if rng.random() < case.true_value else 0

    pre_error = pre_judgment - case.true_value
    post_error = post_judgment - case.true_value

    pre_abs_error = abs(pre_error)
    post_abs_error = abs(post_error)
    error_reduction = pre_abs_error - post_abs_error

    pre_brier = brier_score(pre_judgment, outcome)
    post_brier = brier_score(post_judgment, outcome)
    brier_improvement = pre_brier - post_brier

    review = (
        post_abs_error > 0.15
        or post_brier > 0.25
        or error_reduction < 0
        or (case.decision_stakes == "high" and case.evidence_quality == "low")
    )

    return {
        "case_id": case.case_id,
        "domain": case.domain,
        "bias_source": case.bias_source,
        "hygiene_practice": case.hygiene_practice,
        "true_value": round(case.true_value, 6),
        "evidence_quality": case.evidence_quality,
        "decision_stakes": case.decision_stakes,
        "pre_hygiene_judgment": round(pre_judgment, 6),
        "post_hygiene_judgment": round(post_judgment, 6),
        "outcome": outcome,
        "pre_error": round(pre_error, 6),
        "post_error": round(post_error, 6),
        "pre_absolute_error": round(pre_abs_error, 6),
        "post_absolute_error": round(post_abs_error, 6),
        "error_reduction": round(error_reduction, 6),
        "pre_brier_score": round(pre_brier, 6),
        "post_brier_score": round(post_brier, 6),
        "brier_improvement": round(brier_improvement, 6),
        "post_probability_bin": probability_bin(post_judgment),
        "review_flag": "review" if review else "acceptable",
    }


def summarize_by(rows: list[dict[str, object]], field: str) -> list[dict[str, object]]:
    output: list[dict[str, object]] = []

    for group in sorted({str(row[field]) for row in rows}):
        subset = [row for row in rows if str(row[field]) == group]
        pre_errors = [float(row["pre_error"]) for row in subset]
        post_errors = [float(row["post_error"]) for row in subset]

        pre_bias = mean(pre_errors)
        post_bias = mean(post_errors)
        pre_noise = stdev(pre_errors) if len(pre_errors) > 1 else 0.0
        post_noise = stdev(post_errors) if len(post_errors) > 1 else 0.0

        pre_mse = mean(error ** 2 for error in pre_errors)
        post_mse = mean(error ** 2 for error in post_errors)

        output.append({
            field: group,
            "n_cases": len(subset),
            "pre_bias": round(pre_bias, 6),
            "post_bias": round(post_bias, 6),
            "bias_reduction": round(abs(pre_bias) - abs(post_bias), 6),
            "pre_noise": round(pre_noise, 6),
            "post_noise": round(post_noise, 6),
            "noise_reduction": round(pre_noise - post_noise, 6),
            "pre_mse": round(pre_mse, 6),
            "post_mse": round(post_mse, 6),
            "mse_reduction": round(pre_mse - post_mse, 6),
            "mean_error_reduction": round(mean(float(row["error_reduction"]) for row in subset), 6),
            "mean_brier_improvement": round(mean(float(row["brier_improvement"]) for row in subset), 6),
            "review_rate": round(sum(1 for row in subset if row["review_flag"] == "review") / len(subset), 6),
        })

    return output


def calibration_table(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    output: list[dict[str, object]] = []
    n_total = len(rows)

    for bin_name in sorted({str(row["post_probability_bin"]) for row in rows}):
        subset = [row for row in rows if row["post_probability_bin"] == bin_name]
        avg_probability = mean(float(row["post_hygiene_judgment"]) for row in subset)
        observed_frequency = mean(int(row["outcome"]) for row in subset)
        abs_gap = abs(avg_probability - observed_frequency)

        output.append({
            "probability_bin": bin_name,
            "n_cases": len(subset),
            "average_probability": round(avg_probability, 6),
            "observed_frequency": round(observed_frequency, 6),
            "calibration_gap": round(avg_probability - observed_frequency, 6),
            "absolute_calibration_gap": round(abs_gap, 6),
            "weighted_calibration_error": round((len(subset) / n_total) * abs_gap, 6),
            "average_brier_score": round(mean(float(row["post_brier_score"]) for row in subset), 6),
        })

    return output


def overall_metrics(rows: list[dict[str, object]], calibration_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    pre_errors = [float(row["pre_error"]) for row in rows]
    post_errors = [float(row["post_error"]) for row in rows]

    pre_bias = mean(pre_errors)
    post_bias = mean(post_errors)
    pre_noise = stdev(pre_errors)
    post_noise = stdev(post_errors)
    pre_mse = mean(error ** 2 for error in pre_errors)
    post_mse = mean(error ** 2 for error in post_errors)

    return [
        {"metric": "pre_bias", "value": round(pre_bias, 6)},
        {"metric": "post_bias", "value": round(post_bias, 6)},
        {"metric": "bias_reduction", "value": round(abs(pre_bias) - abs(post_bias), 6)},
        {"metric": "pre_noise", "value": round(pre_noise, 6)},
        {"metric": "post_noise", "value": round(post_noise, 6)},
        {"metric": "noise_reduction", "value": round(pre_noise - post_noise, 6)},
        {"metric": "pre_mse", "value": round(pre_mse, 6)},
        {"metric": "post_mse", "value": round(post_mse, 6)},
        {"metric": "mse_reduction", "value": round(pre_mse - post_mse, 6)},
        {"metric": "expected_calibration_error", "value": round(sum(float(row["weighted_calibration_error"]) for row in calibration_rows), 6)},
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

    domain_rows = summarize_by(rows, "domain")
    practice_rows = summarize_by(rows, "hygiene_practice")
    bias_source_rows = summarize_by(rows, "bias_source")
    calibration_rows = calibration_table(rows)
    review_rows = [row for row in rows if row["review_flag"] == "review"]
    metrics = overall_metrics(rows, calibration_rows)

    write_csv(TABLES / "decision_hygiene_cases.csv", rows)
    write_csv(TABLES / "domain_decision_hygiene_summary.csv", domain_rows)
    write_csv(TABLES / "hygiene_practice_summary.csv", practice_rows)
    write_csv(TABLES / "bias_source_summary.csv", bias_source_rows)
    write_csv(TABLES / "decision_hygiene_calibration_table.csv", calibration_rows)
    write_csv(TABLES / "decision_hygiene_review_queue.csv", review_rows)
    write_csv(TABLES / "overall_decision_hygiene_metrics.csv", metrics)

    write_json(
        RECORDS / "decision_hygiene_record.json",
        {
            "article": "Decision Hygiene and Bias Reduction",
            "decision_context": "Evaluating whether decision hygiene practices reduce bias, noise, mean squared error, miscalibration, and review risk.",
            "modeling_principles": [
                "Decision hygiene should reduce predictable bias and unwanted noise.",
                "Bias reduction should be measured, not merely asserted.",
                "Independent estimates, base-rate checks, structured dissent, calibration review, decision records, and model validation support cleaner judgment.",
                "Decision records should preserve assumptions, uncertainty, dissent, confidence, and review triggers.",
                "Bias reduction should be scaled to stakes, uncertainty, reversibility, and harm potential."
            ],
            "overall_metrics": metrics,
            "domain_summary": domain_rows,
            "practice_summary": practice_rows,
            "bias_source_summary": bias_source_rows,
            "calibration_summary": calibration_rows,
            "review_queue_size": len(review_rows),
        },
    )

    print("Decision hygiene and bias reduction workflow complete.")
    print(TABLES / "decision_hygiene_cases.csv")
    print(TABLES / "domain_decision_hygiene_summary.csv")
    print(TABLES / "hygiene_practice_summary.csv")
    print(TABLES / "decision_hygiene_calibration_table.csv")
    print(TABLES / "decision_hygiene_review_queue.csv")
    print(RECORDS / "decision_hygiene_record.json")


if __name__ == "__main__":
    main()
