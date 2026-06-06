#!/usr/bin/env python3
"""
Framing Effects in Decision-Making Simulation

Simulates equivalent gain and loss frames, reference-point sensitivity,
prospect-style valuation, frame reversals, domain diagnostics, review
queues, and decision-record export.

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
class FramingCase:
    case_id: int
    domain: str
    reference_point: float
    sure_outcome: float
    risky_high_outcome: float
    risky_high_probability: float
    loss_aversion: float
    alpha: float
    beta: float


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def load_seed_cases() -> list[FramingCase]:
    rows = read_csv_dicts(DATA / "synthetic_framing_cases.csv")
    return [
        FramingCase(
            case_id=int(row["case_id"]),
            domain=row["domain"],
            reference_point=float(row["reference_point"]),
            sure_outcome=float(row["sure_outcome"]),
            risky_high_outcome=float(row["risky_high_outcome"]),
            risky_high_probability=float(row["risky_high_probability"]),
            loss_aversion=float(row["loss_aversion"]),
            alpha=float(row["alpha"]),
            beta=float(row["beta"]),
        )
        for row in rows
    ]


def prospect_value(x: float, alpha: float, beta: float, loss_aversion: float) -> float:
    if x >= 0:
        return x ** alpha
    return -loss_aversion * ((-x) ** beta)


def expected_value(high: float, high_probability: float, low: float = 0.0) -> float:
    return high * high_probability + low * (1.0 - high_probability)


def prospect_score(
    high: float,
    high_probability: float,
    low: float,
    reference_point: float,
    alpha: float,
    beta: float,
    loss_aversion: float,
) -> float:
    low_probability = 1.0 - high_probability
    return (
        high_probability * prospect_value(high - reference_point, alpha, beta, loss_aversion)
        + low_probability * prospect_value(low - reference_point, alpha, beta, loss_aversion)
    )


def generate_cases(n: int = 800, seed: int = 42) -> list[FramingCase]:
    rng = random.Random(seed)
    domains = [
        "Healthcare",
        "Public Policy",
        "Financial Risk",
        "Infrastructure",
        "AI Governance",
        "Organizational Strategy",
    ]
    reference_points = [-100.0, 0.0, 100.0]
    cases = load_seed_cases()

    for case_id in range(len(cases) + 1, n + 1):
        cases.append(
            FramingCase(
                case_id=case_id,
                domain=rng.choice(domains),
                reference_point=rng.choices(reference_points, weights=[0.25, 0.50, 0.25], k=1)[0],
                sure_outcome=rng.choice([80.0, 120.0, 160.0, 200.0]),
                risky_high_outcome=rng.choice([180.0, 240.0, 300.0, 360.0]),
                risky_high_probability=rng.uniform(0.45, 0.85),
                loss_aversion=rng.uniform(1.4, 2.8),
                alpha=rng.uniform(0.75, 0.95),
                beta=rng.uniform(0.75, 0.95),
            )
        )

    return cases


def evaluate_case(case: FramingCase) -> dict[str, object]:
    risky_low = 0.0

    sure_gain = case.sure_outcome
    risky_gain_high = case.risky_high_outcome
    risky_gain_low = risky_low

    sure_loss = -case.sure_outcome
    risky_loss_high = -case.risky_high_outcome
    risky_loss_low = risky_low

    ev_sure_gain = sure_gain
    ev_risky_gain = expected_value(risky_gain_high, case.risky_high_probability, risky_gain_low)
    ev_sure_loss = sure_loss
    ev_risky_loss = expected_value(risky_loss_high, case.risky_high_probability, risky_loss_low)

    prospect_sure_gain = prospect_score(
        sure_gain, 1.0, 0.0, case.reference_point, case.alpha, case.beta, case.loss_aversion
    )
    prospect_risky_gain = prospect_score(
        risky_gain_high, case.risky_high_probability, risky_gain_low, case.reference_point,
        case.alpha, case.beta, case.loss_aversion
    )
    prospect_sure_loss = prospect_score(
        sure_loss, 1.0, 0.0, case.reference_point, case.alpha, case.beta, case.loss_aversion
    )
    prospect_risky_loss = prospect_score(
        risky_loss_high, case.risky_high_probability, risky_loss_low, case.reference_point,
        case.alpha, case.beta, case.loss_aversion
    )

    gain_frame_choice = "sure option" if prospect_sure_gain >= prospect_risky_gain else "risky option"
    loss_frame_choice = "sure option" if prospect_sure_loss >= prospect_risky_loss else "risky option"

    frame_reversal = gain_frame_choice != loss_frame_choice
    gain_risk_premium = prospect_risky_gain - prospect_sure_gain
    loss_risk_premium = prospect_risky_loss - prospect_sure_loss
    frame_sensitivity_index = abs(gain_risk_premium - loss_risk_premium)

    return {
        "case_id": case.case_id,
        "domain": case.domain,
        "reference_point": case.reference_point,
        "sure_outcome": case.sure_outcome,
        "risky_high_outcome": case.risky_high_outcome,
        "risky_high_probability": round(case.risky_high_probability, 6),
        "loss_aversion": round(case.loss_aversion, 6),
        "alpha": round(case.alpha, 6),
        "beta": round(case.beta, 6),
        "ev_sure_gain": round(ev_sure_gain, 6),
        "ev_risky_gain": round(ev_risky_gain, 6),
        "ev_sure_loss": round(ev_sure_loss, 6),
        "ev_risky_loss": round(ev_risky_loss, 6),
        "prospect_sure_gain": round(prospect_sure_gain, 6),
        "prospect_risky_gain": round(prospect_risky_gain, 6),
        "prospect_sure_loss": round(prospect_sure_loss, 6),
        "prospect_risky_loss": round(prospect_risky_loss, 6),
        "gain_frame_choice": gain_frame_choice,
        "loss_frame_choice": loss_frame_choice,
        "frame_reversal": frame_reversal,
        "gain_risk_premium": round(gain_risk_premium, 6),
        "loss_risk_premium": round(loss_risk_premium, 6),
        "frame_sensitivity_index": round(frame_sensitivity_index, 6),
    }


def add_review_flags(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    sensitivities = sorted(float(row["frame_sensitivity_index"]) for row in rows)
    threshold = sensitivities[int(0.80 * (len(sensitivities) - 1))]

    flagged_rows: list[dict[str, object]] = []
    for row in rows:
        review = bool(row["frame_reversal"]) or float(row["frame_sensitivity_index"]) >= threshold
        new_row = dict(row)
        new_row["review_flag"] = "review" if review else "acceptable"
        flagged_rows.append(new_row)

    return flagged_rows


def group_summary(rows: list[dict[str, object]], group_field: str) -> list[dict[str, object]]:
    output: list[dict[str, object]] = []

    for group in sorted({row[group_field] for row in rows}):
        subset = [row for row in rows if row[group_field] == group]
        output.append({
            group_field: group,
            "n_cases": len(subset),
            "frame_reversal_rate": round(sum(1 for row in subset if row["frame_reversal"]) / len(subset), 6),
            "average_frame_sensitivity_index": round(mean(float(row["frame_sensitivity_index"]) for row in subset), 6),
            "gain_risky_choice_rate": round(sum(1 for row in subset if row["gain_frame_choice"] == "risky option") / len(subset), 6),
            "loss_risky_choice_rate": round(sum(1 for row in subset if row["loss_frame_choice"] == "risky option") / len(subset), 6),
            "review_rate": round(sum(1 for row in subset if row["review_flag"] == "review") / len(subset), 6),
        })

    return output


def attribute_frame_summary() -> list[dict[str, object]]:
    rows = read_csv_dicts(DATA / "synthetic_attribute_frames.csv")
    output: list[dict[str, object]] = []

    for row in rows:
        positive_value = float(row["positive_value"])
        negative_value = float(row["negative_value"])
        equivalence_gap = abs((1.0 - positive_value) - negative_value)
        output.append({
            "attribute_case_id": row["attribute_case_id"],
            "domain": row["domain"],
            "positive_frame": row["positive_frame"],
            "negative_frame": row["negative_frame"],
            "positive_value": positive_value,
            "negative_value": negative_value,
            "equivalence_gap": round(equivalence_gap, 6),
            "review_flag": "review" if equivalence_gap > 0.0001 else "equivalent_pair",
        })

    return output


def risk_communication_summary() -> list[dict[str, object]]:
    rows = read_csv_dicts(DATA / "synthetic_risk_communication_formats.csv")
    output: list[dict[str, object]] = []

    for row in rows:
        baseline = float(row["baseline_risk"])
        new_risk = float(row["new_risk"])
        absolute_change = new_risk - baseline
        relative_change = absolute_change / baseline if baseline else 0.0
        output.append({
            "risk_case_id": row["risk_case_id"],
            "domain": row["domain"],
            "baseline_risk": baseline,
            "new_risk": new_risk,
            "computed_absolute_change": round(absolute_change, 6),
            "computed_relative_change": round(relative_change, 6),
            "preferred_display": row["preferred_display"],
            "format_warning": "show_absolute_and_relative" if abs(relative_change) > 0.25 else "standard_display",
        })

    return output


def overall_metrics(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {"metric": "frame_reversal_rate", "value": round(sum(1 for row in rows if row["frame_reversal"]) / len(rows), 6)},
        {"metric": "average_frame_sensitivity_index", "value": round(mean(float(row["frame_sensitivity_index"]) for row in rows), 6)},
        {"metric": "gain_risky_choice_rate", "value": round(sum(1 for row in rows if row["gain_frame_choice"] == "risky option") / len(rows), 6)},
        {"metric": "loss_risky_choice_rate", "value": round(sum(1 for row in rows if row["loss_frame_choice"] == "risky option") / len(rows), 6)},
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
    cases = generate_cases(n=800, seed=42)
    rows = [evaluate_case(case) for case in cases]
    rows = add_review_flags(rows)

    domain_rows = group_summary(rows, "domain")
    reference_rows = group_summary(rows, "reference_point")
    attribute_rows = attribute_frame_summary()
    risk_rows = risk_communication_summary()
    metric_rows = overall_metrics(rows)
    review_rows = [row for row in rows if row["review_flag"] == "review"]

    write_csv(TABLES / "framing_effects_choice_cases.csv", rows)
    write_csv(TABLES / "domain_framing_diagnostics.csv", domain_rows)
    write_csv(TABLES / "reference_point_sensitivity_summary.csv", reference_rows)
    write_csv(TABLES / "attribute_frame_equivalence_checks.csv", attribute_rows)
    write_csv(TABLES / "risk_communication_format_summary.csv", risk_rows)
    write_csv(TABLES / "framing_review_queue.csv", review_rows)
    write_csv(TABLES / "overall_framing_effects_metrics.csv", metric_rows)

    write_json(
        RECORDS / "framing_effects_decision_record.json",
        {
            "article": "Framing Effects in Decision-Making",
            "decision_context": "Testing whether equivalent gain and loss frames produce different choices and whether reference-point shifts alter valuation.",
            "modeling_principles": [
                "Equivalent outcome descriptions should be tested under multiple frames.",
                "Reference points should be made explicit.",
                "Gain and loss frames can change risk preference.",
                "Absolute and relative risk formats should be shown together when decision-relevant.",
                "Frame-sensitive decisions should be reviewed before action.",
                "Decision records should preserve the frame used at the time of choice.",
            ],
            "overall_metrics": metric_rows,
            "domain_summary": domain_rows,
            "reference_point_summary": reference_rows,
            "attribute_frame_summary": attribute_rows,
            "risk_communication_summary": risk_rows,
            "review_queue_size": len(review_rows),
        },
    )

    print("Framing effects decision-making workflow complete.")
    print(TABLES / "framing_effects_choice_cases.csv")
    print(TABLES / "domain_framing_diagnostics.csv")
    print(TABLES / "reference_point_sensitivity_summary.csv")
    print(TABLES / "framing_review_queue.csv")
    print(RECORDS / "framing_effects_decision_record.json")


if __name__ == "__main__":
    main()
