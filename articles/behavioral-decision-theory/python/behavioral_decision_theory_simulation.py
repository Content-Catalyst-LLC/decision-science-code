#!/usr/bin/env python3
"""
Behavioral Decision Theory Simulation

Simulates expected utility, prospect-theory-style scoring, probability
weighting, reference dependence, framing sensitivity, rank divergence,
behavioral review queues, and decision-record export.

Uses only the Python standard library.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import csv
import json
import math
import random
from statistics import mean

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
DATA = ARTICLE_ROOT / "data"
TABLES = ARTICLE_ROOT / "outputs" / "tables"
RECORDS = ARTICLE_ROOT / "outputs" / "decision_records"


@dataclass(frozen=True)
class BehavioralCase:
    case_id: int
    domain: str
    option_name: str
    reference_point: float
    outcome_high: float
    probability_high: float
    outcome_low: float
    loss_aversion: float
    alpha: float
    beta: float
    gamma: float

    @property
    def probability_low(self) -> float:
        return 1.0 - self.probability_high


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def load_seed_cases() -> list[BehavioralCase]:
    rows = read_csv_dicts(DATA / "synthetic_behavioral_cases.csv")
    return [
        BehavioralCase(
            case_id=int(row["case_id"]),
            domain=row["domain"],
            option_name=row["option_name"],
            reference_point=float(row["reference_point"]),
            outcome_high=float(row["outcome_high"]),
            probability_high=float(row["probability_high"]),
            outcome_low=float(row["outcome_low"]),
            loss_aversion=float(row["loss_aversion"]),
            alpha=float(row["alpha"]),
            beta=float(row["beta"]),
            gamma=float(row["gamma"]),
        )
        for row in rows
    ]


def utility(x: float) -> float:
    return math.copysign(math.sqrt(abs(x)), x)


def prospect_value(x: float, alpha: float, beta: float, loss_aversion: float) -> float:
    if x >= 0:
        return x ** alpha
    return -loss_aversion * ((-x) ** beta)


def weighted_probability(p: float, gamma: float) -> float:
    p = max(0.000001, min(0.999999, p))
    numerator = p ** gamma
    denominator = (p ** gamma + (1.0 - p) ** gamma) ** (1.0 / gamma)
    return numerator / denominator


def generate_cases(n: int = 720, seed: int = 42) -> list[BehavioralCase]:
    rng = random.Random(seed)
    domains = [
        "Public Policy",
        "Healthcare",
        "Financial Risk",
        "Infrastructure",
        "AI Governance",
        "Organizational Strategy",
    ]
    option_names = [
        "Status Quo",
        "Cautious Alternative",
        "Balanced Alternative",
        "High-Upside Alternative",
        "Loss-Avoidance Alternative",
    ]

    cases = load_seed_cases()

    for case_id in range(len(cases) + 1, n + 1):
        cases.append(
            BehavioralCase(
                case_id=case_id,
                domain=rng.choice(domains),
                option_name=rng.choice(option_names),
                reference_point=rng.choices([-100.0, 0.0, 100.0], weights=[0.25, 0.50, 0.25], k=1)[0],
                outcome_high=rng.choice([80.0, 120.0, 180.0, 240.0, 320.0]),
                probability_high=rng.uniform(0.10, 0.90),
                outcome_low=rng.choice([-160.0, -80.0, 0.0, 40.0]),
                loss_aversion=rng.uniform(1.4, 3.0),
                alpha=rng.uniform(0.75, 0.95),
                beta=rng.uniform(0.75, 0.95),
                gamma=rng.uniform(0.55, 0.95),
            )
        )

    return cases


def evaluate_case(case: BehavioralCase) -> dict[str, object]:
    expected_value = (
        case.outcome_high * case.probability_high
        + case.outcome_low * case.probability_low
    )

    expected_utility = (
        case.probability_high * utility(case.outcome_high)
        + case.probability_low * utility(case.outcome_low)
    )

    weighted_high = weighted_probability(case.probability_high, case.gamma)
    weighted_low = weighted_probability(case.probability_low, case.gamma)

    prospect_score = (
        weighted_high
        * prospect_value(
            case.outcome_high - case.reference_point,
            case.alpha,
            case.beta,
            case.loss_aversion,
        )
        + weighted_low
        * prospect_value(
            case.outcome_low - case.reference_point,
            case.alpha,
            case.beta,
            case.loss_aversion,
        )
    )

    gain_frame_score = (
        weighted_high
        * prospect_value(abs(case.outcome_high), case.alpha, case.beta, case.loss_aversion)
        + weighted_low
        * prospect_value(abs(case.outcome_low), case.alpha, case.beta, case.loss_aversion)
    )

    loss_frame_score = (
        weighted_high
        * prospect_value(-abs(case.outcome_high), case.alpha, case.beta, case.loss_aversion)
        + weighted_low
        * prospect_value(-abs(case.outcome_low), case.alpha, case.beta, case.loss_aversion)
    )

    probability_weight_distortion = abs(weighted_high - case.probability_high)
    frame_sensitivity_index = abs(gain_frame_score - loss_frame_score)

    return {
        "case_id": case.case_id,
        "domain": case.domain,
        "option_name": case.option_name,
        "reference_point": case.reference_point,
        "outcome_high": case.outcome_high,
        "probability_high": round(case.probability_high, 6),
        "outcome_low": case.outcome_low,
        "probability_low": round(case.probability_low, 6),
        "loss_aversion": round(case.loss_aversion, 6),
        "alpha": round(case.alpha, 6),
        "beta": round(case.beta, 6),
        "gamma": round(case.gamma, 6),
        "expected_value": round(expected_value, 6),
        "expected_utility": round(expected_utility, 6),
        "weighted_high": round(weighted_high, 6),
        "weighted_low": round(weighted_low, 6),
        "prospect_score": round(prospect_score, 6),
        "gain_frame_score": round(gain_frame_score, 6),
        "loss_frame_score": round(loss_frame_score, 6),
        "probability_weight_distortion": round(probability_weight_distortion, 6),
        "frame_sensitivity_index": round(frame_sensitivity_index, 6),
    }


def percentile(values: list[float], q: float) -> float:
    sorted_values = sorted(values)
    index = int(q * (len(sorted_values) - 1))
    return sorted_values[index]


def add_rank_divergence_and_flags(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    output: list[dict[str, object]] = []

    frame_threshold = percentile([float(row["frame_sensitivity_index"]) for row in rows], 0.80)
    weight_threshold = percentile([float(row["probability_weight_distortion"]) for row in rows], 0.80)

    for domain in sorted({str(row["domain"]) for row in rows}):
        subset = [row for row in rows if row["domain"] == domain]

        eu_sorted = sorted(subset, key=lambda row: float(row["expected_utility"]), reverse=True)
        prospect_sorted = sorted(subset, key=lambda row: float(row["prospect_score"]), reverse=True)

        eu_ranks = {int(row["case_id"]): rank for rank, row in enumerate(eu_sorted, start=1)}
        prospect_ranks = {int(row["case_id"]): rank for rank, row in enumerate(prospect_sorted, start=1)}

        for row in subset:
            case_id = int(row["case_id"])
            rank_divergence = eu_ranks[case_id] - prospect_ranks[case_id]
            new_row = dict(row)
            new_row["expected_utility_rank"] = eu_ranks[case_id]
            new_row["prospect_score_rank"] = prospect_ranks[case_id]
            new_row["rank_divergence"] = rank_divergence

            review = (
                abs(rank_divergence) > 25
                or float(row["frame_sensitivity_index"]) >= frame_threshold
                or float(row["probability_weight_distortion"]) >= weight_threshold
                or float(row["loss_aversion"]) >= 2.5
            )

            new_row["review_flag"] = "review" if review else "acceptable"
            output.append(new_row)

    return sorted(output, key=lambda row: int(row["case_id"]))


def group_summary(rows: list[dict[str, object]], field: str) -> list[dict[str, object]]:
    output: list[dict[str, object]] = []

    for group in sorted({row[field] for row in rows}):
        subset = [row for row in rows if row[field] == group]
        output.append({
            field: group,
            "n_cases": len(subset),
            "average_expected_value": round(mean(float(row["expected_value"]) for row in subset), 6),
            "average_expected_utility": round(mean(float(row["expected_utility"]) for row in subset), 6),
            "average_prospect_score": round(mean(float(row["prospect_score"]) for row in subset), 6),
            "average_probability_weight_distortion": round(mean(float(row["probability_weight_distortion"]) for row in subset), 6),
            "average_frame_sensitivity_index": round(mean(float(row["frame_sensitivity_index"]) for row in subset), 6),
            "average_absolute_rank_divergence": round(mean(abs(float(row["rank_divergence"])) for row in subset), 6),
            "review_rate": round(sum(1 for row in subset if row["review_flag"] == "review") / len(subset), 6),
        })

    return output


def framing_equivalence_summary() -> list[dict[str, object]]:
    rows = read_csv_dicts(DATA / "synthetic_framing_cases.csv")
    output: list[dict[str, object]] = []

    for row in rows:
        positive_value = float(row["positive_value"])
        negative_value = float(row["negative_value"])
        equivalence_gap = abs((1.0 - positive_value) - negative_value)
        output.append({
            "frame_id": row["frame_id"],
            "frame_type": row["frame_type"],
            "domain": row["domain"],
            "positive_frame": row["positive_frame"],
            "negative_frame": row["negative_frame"],
            "positive_value": positive_value,
            "negative_value": negative_value,
            "equivalence_gap": round(equivalence_gap, 6),
            "review_flag": "review" if equivalence_gap > 0.0001 else "equivalent_pair",
        })

    return output


def overall_metrics(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {"metric": "mean_expected_value", "value": round(mean(float(row["expected_value"]) for row in rows), 6)},
        {"metric": "mean_expected_utility", "value": round(mean(float(row["expected_utility"]) for row in rows), 6)},
        {"metric": "mean_prospect_score", "value": round(mean(float(row["prospect_score"]) for row in rows), 6)},
        {"metric": "mean_probability_weight_distortion", "value": round(mean(float(row["probability_weight_distortion"]) for row in rows), 6)},
        {"metric": "mean_frame_sensitivity_index", "value": round(mean(float(row["frame_sensitivity_index"]) for row in rows), 6)},
        {"metric": "mean_absolute_rank_divergence", "value": round(mean(abs(float(row["rank_divergence"])) for row in rows), 6)},
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
    cases = generate_cases(n=720, seed=42)
    rows = [evaluate_case(case) for case in cases]
    rows = add_rank_divergence_and_flags(rows)

    domain_rows = group_summary(rows, "domain")
    reference_rows = group_summary(rows, "reference_point")
    frame_rows = framing_equivalence_summary()
    metrics = overall_metrics(rows)
    review_rows = [row for row in rows if row["review_flag"] == "review"]

    write_csv(TABLES / "behavioral_decision_theory_cases.csv", rows)
    write_csv(TABLES / "domain_behavioral_decision_summary.csv", domain_rows)
    write_csv(TABLES / "reference_point_behavioral_summary.csv", reference_rows)
    write_csv(TABLES / "framing_equivalence_checks.csv", frame_rows)
    write_csv(TABLES / "behavioral_decision_review_queue.csv", review_rows)
    write_csv(TABLES / "overall_behavioral_decision_metrics.csv", metrics)

    write_json(
        RECORDS / "behavioral_decision_theory_decision_record.json",
        {
            "article": "Behavioral Decision Theory",
            "decision_context": "Comparing expected utility and prospect-theory-style behavioral valuation under reference dependence, loss aversion, probability weighting, and framing effects.",
            "modeling_principles": [
                "Formal models should be paired with behavioral diagnostics.",
                "Reference points should be made explicit.",
                "Loss aversion and framing can change apparent preferences.",
                "Probability weighting can distort risk perception.",
                "Behavioral divergence should trigger review before high-stakes decisions.",
                "Decision records should preserve frames, assumptions, behavioral flags, and rationale."
            ],
            "overall_metrics": metrics,
            "domain_summary": domain_rows,
            "reference_point_summary": reference_rows,
            "framing_equivalence_summary": frame_rows,
            "review_queue_size": len(review_rows),
        },
    )

    print("Behavioral decision theory workflow complete.")
    print(TABLES / "behavioral_decision_theory_cases.csv")
    print(TABLES / "domain_behavioral_decision_summary.csv")
    print(TABLES / "reference_point_behavioral_summary.csv")
    print(TABLES / "behavioral_decision_review_queue.csv")
    print(RECORDS / "behavioral_decision_theory_decision_record.json")


if __name__ == "__main__":
    main()
