#!/usr/bin/env python3
"""
Probability Calibration and Decision Confidence Simulation

Computes Brier scores, log loss, reliability tables, expected
calibration error, confidence-bias diagnostics, base-rate comparisons,
decision-threshold calibration, and a decision-record JSON file.

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
class Forecast:
    forecast_id: int
    domain: str
    forecast_probability: float
    true_probability: float
    outcome: int
    confidence_profile: str


def clamp(value: float, low: float = 0.01, high: float = 0.99) -> float:
    return max(low, min(high, value))


def probability_bin(probability: float) -> str:
    if probability >= 1.0:
        return "[0.9,1.0]"
    lower = int(probability * 10) / 10
    upper = min(1.0, lower + 0.1)
    right = "]" if upper >= 1.0 else ")"
    return f"[{lower:.1f},{upper:.1f}{right}"


def generate_forecasts(n: int = 1200, seed: int = 42) -> list[Forecast]:
    rng = random.Random(seed)
    domains = [
        "Strategic Forecast",
        "Risk Forecast",
        "Operational Forecast",
        "Policy Forecast",
        "Model Governance Forecast",
    ]
    profiles = ["well calibrated", "overconfident", "underconfident"]
    profile_weights = [0.55, 0.30, 0.15]
    forecasts: list[Forecast] = []

    for i in range(1, n + 1):
        domain = rng.choice(domains)
        profile = rng.choices(profiles, weights=profile_weights, k=1)[0]
        base_rate = rng.uniform(0.10, 0.85)
        evidence_strength = rng.uniform(-0.25, 0.25)
        true_probability = clamp(base_rate + evidence_strength, 0.02, 0.98)

        if profile == "overconfident":
            forecast_probability = 0.5 + 1.35 * (true_probability - 0.5)
        elif profile == "underconfident":
            forecast_probability = 0.5 + 0.65 * (true_probability - 0.5)
        else:
            forecast_probability = true_probability

        forecast_probability = clamp(forecast_probability)
        outcome = 1 if rng.random() < true_probability else 0

        forecasts.append(
            Forecast(
                forecast_id=i,
                domain=domain,
                forecast_probability=forecast_probability,
                true_probability=true_probability,
                outcome=outcome,
                confidence_profile=profile,
            )
        )

    return forecasts


def brier_score(probability: float, outcome: int) -> float:
    return (probability - outcome) ** 2


def log_loss(probability: float, outcome: int) -> float:
    probability = clamp(probability)
    return -(outcome * math.log(probability) + (1 - outcome) * math.log(1 - probability))


def forecast_rows(forecasts: list[Forecast]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for forecast in forecasts:
        rows.append({
            "forecast_id": forecast.forecast_id,
            "domain": forecast.domain,
            "forecast_probability": round(forecast.forecast_probability, 6),
            "true_probability": round(forecast.true_probability, 6),
            "outcome": forecast.outcome,
            "confidence_profile": forecast.confidence_profile,
            "brier_component": round(brier_score(forecast.forecast_probability, forecast.outcome), 6),
            "log_loss_component": round(log_loss(forecast.forecast_probability, forecast.outcome), 6),
            "probability_bin": probability_bin(forecast.forecast_probability),
        })
    return rows


def reliability_table(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    bins = sorted({str(row["probability_bin"]) for row in rows})
    output: list[dict[str, object]] = []
    n_total = len(rows)

    for bin_name in bins:
        subset = [row for row in rows if row["probability_bin"] == bin_name]
        average_probability = mean(float(row["forecast_probability"]) for row in subset)
        observed_frequency = mean(int(row["outcome"]) for row in subset)
        absolute_gap = abs(average_probability - observed_frequency)

        output.append({
            "probability_bin": bin_name,
            "n_forecasts": len(subset),
            "average_forecast_probability": round(average_probability, 6),
            "observed_frequency": round(observed_frequency, 6),
            "calibration_gap": round(average_probability - observed_frequency, 6),
            "absolute_calibration_gap": round(absolute_gap, 6),
            "weighted_calibration_error": round((len(subset) / n_total) * absolute_gap, 6),
            "average_brier_score": round(mean(float(row["brier_component"]) for row in subset), 6),
            "average_log_loss": round(mean(float(row["log_loss_component"]) for row in subset), 6),
        })

    return output


def group_summary(rows: list[dict[str, object]], group_field: str) -> list[dict[str, object]]:
    groups = sorted({str(row[group_field]) for row in rows})
    output: list[dict[str, object]] = []

    for group in groups:
        subset = [row for row in rows if row[group_field] == group]
        average_probability = mean(float(row["forecast_probability"]) for row in subset)
        observed_frequency = mean(int(row["outcome"]) for row in subset)
        output.append({
            group_field: group,
            "n_forecasts": len(subset),
            "average_forecast_probability": round(average_probability, 6),
            "observed_frequency": round(observed_frequency, 6),
            "calibration_gap": round(average_probability - observed_frequency, 6),
            "absolute_calibration_gap": round(abs(average_probability - observed_frequency), 6),
            "brier_score": round(mean(float(row["brier_component"]) for row in subset), 6),
            "log_loss": round(mean(float(row["log_loss_component"]) for row in subset), 6),
        })

    return output


def threshold_summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    output: list[dict[str, object]] = []

    for threshold in [0.55, 0.65, 0.75, 0.85]:
        acted = [row for row in rows if float(row["forecast_probability"]) >= threshold]

        if acted:
            average_probability = mean(float(row["forecast_probability"]) for row in acted)
            observed_success_rate = mean(int(row["outcome"]) for row in acted)
            brier = mean(float(row["brier_component"]) for row in acted)
            calibration_gap = average_probability - observed_success_rate
        else:
            average_probability = None
            observed_success_rate = None
            brier = None
            calibration_gap = None

        output.append({
            "decision_threshold": threshold,
            "action_count": len(acted),
            "action_rate": round(len(acted) / len(rows), 6),
            "average_probability_among_acted": None if average_probability is None else round(average_probability, 6),
            "observed_success_rate_among_acted": None if observed_success_rate is None else round(observed_success_rate, 6),
            "threshold_calibration_gap": None if calibration_gap is None else round(calibration_gap, 6),
            "brier_score_among_acted": None if brier is None else round(brier, 6),
        })

    return output


def base_rate_checks(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    reference_rows = read_csv_dicts(DATA / "synthetic_reference_classes.csv")
    reference_lookup = {row["reference_class"]: float(row["base_rate"]) for row in reference_rows}
    output: list[dict[str, object]] = []

    for domain in sorted({str(row["domain"]) for row in rows}):
        subset = [row for row in rows if row["domain"] == domain]
        average_forecast = mean(float(row["forecast_probability"]) for row in subset)
        observed_frequency = mean(int(row["outcome"]) for row in subset)
        base_rate = reference_lookup.get(domain, observed_frequency)
        output.append({
            "domain": domain,
            "reference_class_base_rate": round(base_rate, 6),
            "average_forecast_probability": round(average_forecast, 6),
            "observed_frequency": round(observed_frequency, 6),
            "forecast_minus_base_rate": round(average_forecast - base_rate, 6),
            "observed_minus_base_rate": round(observed_frequency - base_rate, 6),
        })

    return output


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def overall_metrics(rows: list[dict[str, object]], reliability_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {"metric": "overall_brier_score", "value": round(mean(float(row["brier_component"]) for row in rows), 6)},
        {"metric": "overall_log_loss", "value": round(mean(float(row["log_loss_component"]) for row in rows), 6)},
        {"metric": "expected_calibration_error", "value": round(sum(float(row["weighted_calibration_error"]) for row in reliability_rows), 6)},
        {"metric": "average_forecast_probability", "value": round(mean(float(row["forecast_probability"]) for row in rows), 6)},
        {"metric": "observed_frequency", "value": round(mean(int(row["outcome"]) for row in rows), 6)},
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
    forecasts = generate_forecasts(n=1200, seed=42)
    rows = forecast_rows(forecasts)
    reliability_rows = reliability_table(rows)
    domain_rows = group_summary(rows, "domain")
    confidence_rows = group_summary(rows, "confidence_profile")
    threshold_rows = threshold_summary(rows)
    base_rate_rows = base_rate_checks(rows)
    metric_rows = overall_metrics(rows, reliability_rows)

    write_csv(TABLES / "forecast_calibration_observations.csv", rows)
    write_csv(TABLES / "calibration_reliability_table.csv", reliability_rows)
    write_csv(TABLES / "domain_calibration_summary.csv", domain_rows)
    write_csv(TABLES / "confidence_profile_summary.csv", confidence_rows)
    write_csv(TABLES / "decision_threshold_calibration.csv", threshold_rows)
    write_csv(TABLES / "base_rate_reference_class_checks.csv", base_rate_rows)
    write_csv(TABLES / "overall_calibration_metrics.csv", metric_rows)

    write_json(
        RECORDS / "probability_calibration_decision_record.json",
        {
            "article": "Probability Calibration and Decision Confidence",
            "decision_context": "Testing whether stated probabilities match observed outcomes and whether decision thresholds rely on calibrated confidence.",
            "modeling_principles": [
                "Confidence should be expressed as probability or probability range where decision-relevant.",
                "Calibration compares stated probabilities with observed frequencies.",
                "Accuracy, calibration, discrimination, and sharpness are distinct properties.",
                "Base rates and reference classes should discipline probability estimates.",
                "Scoring rules create feedback for probabilistic judgment.",
                "Decision thresholds should use calibrated probabilities, not rhetorical confidence.",
                "Calibration results should be preserved in decision records.",
            ],
            "overall_metrics": metric_rows,
            "reliability_table": reliability_rows,
            "domain_summary": domain_rows,
            "confidence_profile_summary": confidence_rows,
            "threshold_summary": threshold_rows,
            "base_rate_checks": base_rate_rows,
        },
    )

    print("Probability calibration workflow complete.")
    print(TABLES / "calibration_reliability_table.csv")
    print(TABLES / "domain_calibration_summary.csv")
    print(TABLES / "decision_threshold_calibration.csv")
    print(TABLES / "base_rate_reference_class_checks.csv")
    print(RECORDS / "probability_calibration_decision_record.json")


if __name__ == "__main__":
    main()
