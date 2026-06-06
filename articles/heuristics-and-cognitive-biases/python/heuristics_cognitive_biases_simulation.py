#!/usr/bin/env python3
"""
Heuristics and Cognitive Biases Simulation

Simulates anchoring, availability, representativeness, confirmation bias,
overconfidence, calibration error, confidence gaps, domain diagnostics,
and debiasing review queues.

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
    bias_profile: str
    base_rate: float
    evidence_signal: float
    anchor: float
    salience_multiplier: float
    confirming_evidence: float
    disconfirming_evidence: float


def clamp(value: float, low: float = 0.01, high: float = 0.99) -> float:
    return max(low, min(high, value))


def brier_score(probability: float, outcome: int) -> float:
    return (probability - outcome) ** 2


def probability_bin(probability: float) -> str:
    lower = int(probability * 10) / 10
    upper = min(1.0, lower + 0.1)
    right = "]" if upper >= 1.0 else ")"
    return f"[{lower:.1f},{upper:.1f}{right}"


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def load_seed_cases() -> list[JudgmentCase]:
    rows = read_csv_dicts(DATA / "synthetic_judgment_cases.csv")
    return [
        JudgmentCase(
            case_id=int(row["case_id"]),
            domain=row["domain"],
            bias_profile=row["bias_profile"],
            base_rate=float(row["base_rate"]),
            evidence_signal=float(row["evidence_signal"]),
            anchor=float(row["anchor"]),
            salience_multiplier=float(row["salience_multiplier"]),
            confirming_evidence=float(row["confirming_evidence"]),
            disconfirming_evidence=float(row["disconfirming_evidence"]),
        )
        for row in rows
    ]


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
    profiles = [
        "availability",
        "representativeness",
        "anchoring",
        "confirmation",
        "overconfidence",
        "balanced",
    ]
    weights = [0.16, 0.15, 0.16, 0.16, 0.17, 0.20]
    cases = load_seed_cases()

    for case_id in range(len(cases) + 1, n + 1):
        cases.append(
            JudgmentCase(
                case_id=case_id,
                domain=rng.choice(domains),
                bias_profile=rng.choices(profiles, weights=weights, k=1)[0],
                base_rate=rng.uniform(0.10, 0.85),
                evidence_signal=rng.uniform(-0.25, 0.25),
                anchor=rng.uniform(0.20, 0.90),
                salience_multiplier=rng.uniform(0.70, 1.60),
                confirming_evidence=rng.uniform(0.00, 0.30),
                disconfirming_evidence=rng.uniform(0.00, 0.30),
            )
        )

    return cases


def evaluate_case(case: JudgmentCase, rng: random.Random) -> dict[str, object]:
    evidence_based_probability = clamp(case.base_rate + case.evidence_signal)
    judged_probability = evidence_based_probability

    if case.bias_profile == "availability":
        judged_probability = clamp(evidence_based_probability * case.salience_multiplier)

    elif case.bias_profile == "representativeness":
        judged_probability = clamp(0.35 * case.base_rate + 0.65 * evidence_based_probability)

    elif case.bias_profile == "anchoring":
        judged_probability = clamp(0.45 * case.anchor + 0.55 * evidence_based_probability)

    elif case.bias_profile == "confirmation":
        judged_probability = clamp(
            evidence_based_probability
            + 0.80 * case.confirming_evidence
            - 0.35 * case.disconfirming_evidence
        )

    confidence = judged_probability

    if case.bias_profile == "overconfidence":
        confidence = clamp(0.5 + 1.40 * (judged_probability - 0.5))
    else:
        confidence = clamp(judged_probability + rng.gauss(0.0, 0.04))

    outcome = 1 if rng.random() < evidence_based_probability else 0

    score = brier_score(judged_probability, outcome)
    bias_magnitude = abs(judged_probability - evidence_based_probability)
    confidence_gap = confidence - judged_probability

    review_flag = (
        bias_magnitude > 0.12
        or abs(confidence_gap) > 0.12
        or score > 0.25
    )

    return {
        "case_id": case.case_id,
        "domain": case.domain,
        "bias_profile": case.bias_profile,
        "base_rate": round(case.base_rate, 6),
        "evidence_signal": round(case.evidence_signal, 6),
        "evidence_based_probability": round(evidence_based_probability, 6),
        "judged_probability": round(judged_probability, 6),
        "confidence": round(confidence, 6),
        "outcome": outcome,
        "brier_score": round(score, 6),
        "bias_magnitude": round(bias_magnitude, 6),
        "confidence_gap": round(confidence_gap, 6),
        "probability_bin": probability_bin(judged_probability),
        "review_flag": "review" if review_flag else "acceptable",
    }


def group_summary(rows: list[dict[str, object]], field: str) -> list[dict[str, object]]:
    output: list[dict[str, object]] = []

    for group in sorted({str(row[field]) for row in rows}):
        subset = [row for row in rows if row[field] == group]
        output.append({
            field: group,
            "n_cases": len(subset),
            "average_evidence_based_probability": round(mean(float(row["evidence_based_probability"]) for row in subset), 6),
            "average_judged_probability": round(mean(float(row["judged_probability"]) for row in subset), 6),
            "observed_frequency": round(mean(int(row["outcome"]) for row in subset), 6),
            "average_brier_score": round(mean(float(row["brier_score"]) for row in subset), 6),
            "average_bias_magnitude": round(mean(float(row["bias_magnitude"]) for row in subset), 6),
            "average_confidence_gap": round(mean(float(row["confidence_gap"]) for row in subset), 6),
            "review_rate": round(sum(1 for row in subset if row["review_flag"] == "review") / len(subset), 6),
        })

    return output


def calibration_table(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    output: list[dict[str, object]] = []
    n_total = len(rows)

    for bin_name in sorted({str(row["probability_bin"]) for row in rows}):
        subset = [row for row in rows if row["probability_bin"] == bin_name]
        average_probability = mean(float(row["judged_probability"]) for row in subset)
        observed_frequency = mean(int(row["outcome"]) for row in subset)
        absolute_gap = abs(average_probability - observed_frequency)

        output.append({
            "probability_bin": bin_name,
            "n_cases": len(subset),
            "average_judged_probability": round(average_probability, 6),
            "observed_frequency": round(observed_frequency, 6),
            "calibration_gap": round(average_probability - observed_frequency, 6),
            "absolute_calibration_gap": round(absolute_gap, 6),
            "weighted_calibration_error": round((len(subset) / n_total) * absolute_gap, 6),
            "average_brier_score": round(mean(float(row["brier_score"]) for row in subset), 6),
        })

    return output


def overall_metrics(rows: list[dict[str, object]], calibration_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {"metric": "mean_brier_score", "value": round(mean(float(row["brier_score"]) for row in rows), 6)},
        {"metric": "expected_calibration_error", "value": round(sum(float(row["weighted_calibration_error"]) for row in calibration_rows), 6)},
        {"metric": "mean_bias_magnitude", "value": round(mean(float(row["bias_magnitude"]) for row in rows), 6)},
        {"metric": "mean_confidence_gap", "value": round(mean(float(row["confidence_gap"]) for row in rows), 6)},
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

    bias_rows = group_summary(rows, "bias_profile")
    domain_rows = group_summary(rows, "domain")
    calibration_rows = calibration_table(rows)
    metric_rows = overall_metrics(rows, calibration_rows)
    review_rows = [row for row in rows if row["review_flag"] == "review"]

    write_csv(TABLES / "heuristic_judgment_cases.csv", rows)
    write_csv(TABLES / "bias_profile_summary.csv", bias_rows)
    write_csv(TABLES / "domain_bias_diagnostics.csv", domain_rows)
    write_csv(TABLES / "heuristic_calibration_table.csv", calibration_rows)
    write_csv(TABLES / "debiasing_review_queue.csv", review_rows)
    write_csv(TABLES / "overall_bias_diagnostics.csv", metric_rows)

    write_json(
        RECORDS / "heuristics_cognitive_biases_decision_record.json",
        {
            "article": "Heuristics and Cognitive Biases",
            "decision_context": "Diagnosing heuristic distortion, confidence gaps, calibration error, and cases requiring structured debiasing review.",
            "modeling_principles": [
                "Heuristics can be adaptive when matched to valid environments.",
                "Biases are systematic distortions, not merely random mistakes.",
                "Confidence should be calibrated against outcomes.",
                "Base rates and reference classes should discipline judgment.",
                "Independent estimates reduce anchoring and authority effects.",
                "Disconfirming evidence should be actively searched.",
                "Decision records preserve assumptions and reduce hindsight bias.",
            ],
            "overall_metrics": metric_rows,
            "bias_profile_summary": bias_rows,
            "domain_summary": domain_rows,
            "calibration_summary": calibration_rows,
            "review_queue_size": len(review_rows),
        },
    )

    print("Heuristics and cognitive biases workflow complete.")
    print(TABLES / "heuristic_judgment_cases.csv")
    print(TABLES / "bias_profile_summary.csv")
    print(TABLES / "domain_bias_diagnostics.csv")
    print(TABLES / "heuristic_calibration_table.csv")
    print(RECORDS / "heuristics_cognitive_biases_decision_record.json")


if __name__ == "__main__":
    main()
