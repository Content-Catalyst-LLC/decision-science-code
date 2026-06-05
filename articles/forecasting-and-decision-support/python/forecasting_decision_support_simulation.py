#!/usr/bin/env python3
"""
Forecasting and Decision Support Simulation

Computes forecast error metrics, probabilistic calibration,
threshold decisions, value-of-information proxies, horizon summaries,
reference-class checks, early-warning signal flags, and a decision record.

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
class ForecastCase:
    forecast_id: int
    domain: str
    base_rate: float
    true_probability: float
    forecast_probability: float
    outcome: int
    horizon_days: int
    forecast_cost: float
    false_positive_cost: float
    false_negative_cost: float


def clamp(value: float, low: float = 0.01, high: float = 0.99) -> float:
    return max(low, min(high, value))


def brier_score(probability: float, outcome: int) -> float:
    return (probability - outcome) ** 2


def log_loss(probability: float, outcome: int) -> float:
    probability = clamp(probability)
    return -(outcome * math.log(probability) + (1 - outcome) * math.log(1 - probability))


def probability_bin(probability: float) -> str:
    if probability >= 1.0:
        return "[0.9,1.0]"
    lower = int(probability * 10) / 10
    upper = min(1.0, lower + 0.1)
    right = "]" if upper >= 1.0 else ")"
    return f"[{lower:.1f},{upper:.1f}{right}"


def expected_loss(action: bool, probability: float, false_positive_cost: float, false_negative_cost: float) -> float:
    if action:
        return (1.0 - probability) * false_positive_cost
    return probability * false_negative_cost


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def load_seed_forecasts() -> list[ForecastCase]:
    rows = read_csv_dicts(DATA / "synthetic_forecasts.csv")
    return [
        ForecastCase(
            forecast_id=int(row["forecast_id"]),
            domain=row["domain"],
            base_rate=float(row["base_rate"]),
            forecast_probability=float(row["forecast_probability"]),
            true_probability=float(row["true_probability"]),
            outcome=int(row["outcome"]),
            horizon_days=int(row["forecast_horizon_days"]),
            forecast_cost=float(row["forecast_cost"]),
            false_positive_cost=float(row["false_positive_cost"]),
            false_negative_cost=float(row["false_negative_cost"]),
        )
        for row in rows
    ]


def generate_forecasts(n: int = 900, seed: int = 42) -> list[ForecastCase]:
    rng = random.Random(seed)
    domains = [
        "Public Policy",
        "Healthcare",
        "Financial Risk",
        "Infrastructure",
        "AI Governance",
        "Organizational Strategy",
    ]
    horizons = [7, 30, 90, 180, 365]
    cases = load_seed_forecasts()

    for forecast_id in range(len(cases) + 1, n + 1):
        domain = rng.choice(domains)
        base_rate = rng.uniform(0.15, 0.80)
        signal_strength = rng.uniform(-0.20, 0.25)
        horizon_days = rng.choice(horizons)
        horizon_penalty = (horizon_days / 365.0) * rng.uniform(-0.10, 0.10)

        true_probability = clamp(base_rate + signal_strength + horizon_penalty, 0.02, 0.98)
        forecast_probability = clamp(true_probability + rng.gauss(0.0, 0.08))
        outcome = 1 if rng.random() < true_probability else 0

        cases.append(
            ForecastCase(
                forecast_id=forecast_id,
                domain=domain,
                base_rate=base_rate,
                true_probability=true_probability,
                forecast_probability=forecast_probability,
                outcome=outcome,
                horizon_days=horizon_days,
                forecast_cost=rng.uniform(1.0, 12.0),
                false_positive_cost=rng.uniform(5.0, 30.0),
                false_negative_cost=rng.uniform(20.0, 90.0),
            )
        )

    return cases


def forecast_rows(cases: list[ForecastCase]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    for case in cases:
        decision_threshold = case.false_positive_cost / (
            case.false_positive_cost + case.false_negative_cost
        )

        forecast_action = case.forecast_probability >= decision_threshold
        base_rate_action = case.base_rate >= decision_threshold

        loss_with_forecast = expected_loss(
            forecast_action,
            case.forecast_probability,
            case.false_positive_cost,
            case.false_negative_cost,
        )

        loss_without_forecast = expected_loss(
            base_rate_action,
            case.base_rate,
            case.false_positive_cost,
            case.false_negative_cost,
        )

        forecast_value_proxy = loss_without_forecast - loss_with_forecast - case.forecast_cost

        rows.append({
            "forecast_id": case.forecast_id,
            "domain": case.domain,
            "base_rate": round(case.base_rate, 6),
            "true_probability": round(case.true_probability, 6),
            "forecast_probability": round(case.forecast_probability, 6),
            "outcome": case.outcome,
            "forecast_horizon_days": case.horizon_days,
            "probability_bin": probability_bin(case.forecast_probability),
            "brier_score": round(brier_score(case.forecast_probability, case.outcome), 6),
            "log_loss": round(log_loss(case.forecast_probability, case.outcome), 6),
            "decision_threshold": round(decision_threshold, 6),
            "forecast_supported_action": forecast_action,
            "base_rate_action": base_rate_action,
            "expected_loss_with_forecast": round(loss_with_forecast, 6),
            "expected_loss_without_forecast": round(loss_without_forecast, 6),
            "forecast_cost": round(case.forecast_cost, 6),
            "forecast_value_proxy": round(forecast_value_proxy, 6),
        })

    return rows


def calibration_table(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    bins = sorted({str(row["probability_bin"]) for row in rows})
    output: list[dict[str, object]] = []
    n_total = len(rows)

    for bin_name in bins:
        subset = [row for row in rows if row["probability_bin"] == bin_name]
        average_forecast_probability = mean(float(row["forecast_probability"]) for row in subset)
        observed_frequency = mean(int(row["outcome"]) for row in subset)
        absolute_gap = abs(average_forecast_probability - observed_frequency)

        output.append({
            "probability_bin": bin_name,
            "n_forecasts": len(subset),
            "average_forecast_probability": round(average_forecast_probability, 6),
            "observed_frequency": round(observed_frequency, 6),
            "calibration_gap": round(average_forecast_probability - observed_frequency, 6),
            "absolute_calibration_gap": round(absolute_gap, 6),
            "weighted_calibration_error": round((len(subset) / n_total) * absolute_gap, 6),
            "average_brier_score": round(mean(float(row["brier_score"]) for row in subset), 6),
            "average_log_loss": round(mean(float(row["log_loss"]) for row in subset), 6),
        })

    return output


def group_summary(rows: list[dict[str, object]], field: str) -> list[dict[str, object]]:
    groups = sorted({row[field] for row in rows})
    output: list[dict[str, object]] = []

    for group in groups:
        subset = [row for row in rows if row[field] == group]
        output.append({
            field: group,
            "n_forecasts": len(subset),
            "average_forecast_probability": round(mean(float(row["forecast_probability"]) for row in subset), 6),
            "observed_frequency": round(mean(int(row["outcome"]) for row in subset), 6),
            "brier_score": round(mean(float(row["brier_score"]) for row in subset), 6),
            "log_loss": round(mean(float(row["log_loss"]) for row in subset), 6),
            "average_forecast_value_proxy": round(mean(float(row["forecast_value_proxy"]) for row in subset), 6),
            "positive_forecast_value_rate": round(sum(1 for row in subset if float(row["forecast_value_proxy"]) > 0) / len(subset), 6),
            "forecast_action_rate": round(sum(1 for row in subset if bool(row["forecast_supported_action"])) / len(subset), 6),
            "base_rate_action_rate": round(sum(1 for row in subset if bool(row["base_rate_action"])) / len(subset), 6),
        })

    return output


def threshold_summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    output: list[dict[str, object]] = []

    for threshold in [0.25, 0.40, 0.55, 0.70, 0.85]:
        acted = [row for row in rows if float(row["forecast_probability"]) >= threshold]
        if acted:
            observed_frequency = mean(int(row["outcome"]) for row in acted)
            average_probability = mean(float(row["forecast_probability"]) for row in acted)
            average_brier = mean(float(row["brier_score"]) for row in acted)
        else:
            observed_frequency = None
            average_probability = None
            average_brier = None

        output.append({
            "threshold": threshold,
            "action_rate": round(len(acted) / len(rows), 6),
            "observed_frequency_among_acted": None if observed_frequency is None else round(observed_frequency, 6),
            "average_probability_among_acted": None if average_probability is None else round(average_probability, 6),
            "average_brier_among_acted": None if average_brier is None else round(average_brier, 6),
        })

    return output


def base_rate_reference_checks(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    reference_rows = read_csv_dicts(DATA / "synthetic_reference_classes.csv")
    reference_lookup = {row["reference_class"]: float(row["base_rate"]) for row in reference_rows}
    output: list[dict[str, object]] = []

    for domain in sorted({str(row["domain"]) for row in rows}):
        subset = [row for row in rows if row["domain"] == domain]
        average_forecast_probability = mean(float(row["forecast_probability"]) for row in subset)
        observed_frequency = mean(int(row["outcome"]) for row in subset)
        base_rate = reference_lookup.get(domain, observed_frequency)

        output.append({
            "domain": domain,
            "reference_class_base_rate": round(base_rate, 6),
            "average_forecast_probability": round(average_forecast_probability, 6),
            "observed_frequency": round(observed_frequency, 6),
            "forecast_minus_base_rate": round(average_forecast_probability - base_rate, 6),
            "observed_minus_base_rate": round(observed_frequency - base_rate, 6),
        })

    return output


def early_warning_summary() -> list[dict[str, object]]:
    rows = read_csv_dicts(DATA / "synthetic_early_warning_signals.csv")
    output: list[dict[str, object]] = []

    for row in rows:
        current_value = float(row["current_value"])
        review_threshold = float(row["review_threshold"])
        direction = row["direction"]

        if direction == "above":
            triggered = current_value >= review_threshold
        elif direction == "below":
            triggered = current_value <= review_threshold
        else:
            triggered = False

        output.append({
            "signal_id": row["signal_id"],
            "domain": row["domain"],
            "indicator": row["indicator"],
            "current_value": current_value,
            "review_threshold": review_threshold,
            "direction": direction,
            "triggered": triggered,
            "interpretation": row["interpretation"],
        })

    return output


def overall_metrics(rows: list[dict[str, object]], calibration_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {"metric": "overall_brier_score", "value": round(mean(float(row["brier_score"]) for row in rows), 6)},
        {"metric": "overall_log_loss", "value": round(mean(float(row["log_loss"]) for row in rows), 6)},
        {"metric": "expected_calibration_error", "value": round(sum(float(row["weighted_calibration_error"]) for row in calibration_rows), 6)},
        {"metric": "average_forecast_value_proxy", "value": round(mean(float(row["forecast_value_proxy"]) for row in rows), 6)},
        {"metric": "positive_forecast_value_rate", "value": round(sum(1 for row in rows if float(row["forecast_value_proxy"]) > 0) / len(rows), 6)},
        {"metric": "forecast_action_rate", "value": round(sum(1 for row in rows if bool(row["forecast_supported_action"])) / len(rows), 6)},
        {"metric": "base_rate_action_rate", "value": round(sum(1 for row in rows if bool(row["base_rate_action"])) / len(rows), 6)},
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
    cases = generate_forecasts(n=900, seed=42)
    rows = forecast_rows(cases)
    calibration_rows = calibration_table(rows)
    domain_rows = group_summary(rows, "domain")
    horizon_rows = group_summary(rows, "forecast_horizon_days")
    threshold_rows = threshold_summary(rows)
    base_rate_rows = base_rate_reference_checks(rows)
    early_warning_rows = early_warning_summary()
    metric_rows = overall_metrics(rows, calibration_rows)

    write_csv(TABLES / "forecast_decision_observations.csv", rows)
    write_csv(TABLES / "forecast_calibration_table.csv", calibration_rows)
    write_csv(TABLES / "domain_forecast_decision_support_summary.csv", domain_rows)
    write_csv(TABLES / "forecast_horizon_summary.csv", horizon_rows)
    write_csv(TABLES / "forecast_threshold_summary.csv", threshold_rows)
    write_csv(TABLES / "base_rate_reference_class_checks.csv", base_rate_rows)
    write_csv(TABLES / "early_warning_signal_summary.csv", early_warning_rows)
    write_csv(TABLES / "overall_forecast_decision_metrics.csv", metric_rows)

    write_json(
        RECORDS / "forecasting_decision_support_record.json",
        {
            "article": "Forecasting and Decision Support",
            "decision_context": "Using probabilistic forecasts to support threshold decisions, expected-loss reduction, monitoring, and accountable decision records.",
            "modeling_principles": [
                "Forecasts should be tied to explicit decisions.",
                "Forecasts should represent uncertainty rather than only point estimates.",
                "Forecast quality should include calibration, error, horizon, and decision value.",
                "Thresholds should connect forecast probabilities to action.",
                "Forecast value depends on whether the forecast improves decisions after accounting for cost.",
                "Decision records should preserve forecasts, assumptions, thresholds, outcomes, and review triggers.",
            ],
            "overall_metrics": metric_rows,
            "domain_summary": domain_rows,
            "horizon_summary": horizon_rows,
            "threshold_summary": threshold_rows,
            "base_rate_reference_checks": base_rate_rows,
            "early_warning_signals": early_warning_rows,
        },
    )

    print("Forecasting and decision support workflow complete.")
    print(TABLES / "forecast_decision_observations.csv")
    print(TABLES / "forecast_calibration_table.csv")
    print(TABLES / "domain_forecast_decision_support_summary.csv")
    print(TABLES / "forecast_horizon_summary.csv")
    print(TABLES / "base_rate_reference_class_checks.csv")
    print(RECORDS / "forecasting_decision_support_record.json")


if __name__ == "__main__":
    main()
