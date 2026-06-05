#!/usr/bin/env python3
"""
Risk Analysis and Probabilistic Reasoning Simulation

Computes expected loss, volatility, threshold breach probability,
VaR, CVaR, stress-test results, probability-quality summaries,
and a decision-record JSON file.

Uses only the Python standard library.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import csv
import json
import random
from statistics import mean, pstdev

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
DATA = ARTICLE_ROOT / "data"
TABLES = ARTICLE_ROOT / "outputs" / "tables"
RECORDS = ARTICLE_ROOT / "outputs" / "decision_records"

QUALITY_SCORES = {
    "high": 1.00,
    "medium": 0.65,
    "low": 0.35,
}


@dataclass(frozen=True)
class Strategy:
    name: str
    mean_return: float
    volatility: float
    shock_probability: float
    shock_size: float
    recovery_credit: float
    description: str


@dataclass(frozen=True)
class StressScenario:
    name: str
    return_shift: float
    volatility_multiplier: float
    shock_multiplier: float
    description: str


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def load_strategies() -> list[Strategy]:
    rows = read_csv_dicts(DATA / "synthetic_risk_strategies.csv")
    return [
        Strategy(
            row["strategy"],
            float(row["mean_return"]),
            float(row["volatility"]),
            float(row["shock_probability"]),
            float(row["shock_size"]),
            float(row["recovery_credit"]),
            row["description"],
        )
        for row in rows
    ]


def load_scenarios() -> list[StressScenario]:
    rows = read_csv_dicts(DATA / "synthetic_stress_scenarios.csv")
    return [
        StressScenario(
            row["scenario"],
            float(row["return_shift"]),
            float(row["volatility_multiplier"]),
            float(row["shock_multiplier"]),
            row["description"],
        )
        for row in rows
    ]


def simulate_strategy(strategy: Strategy, trials: int = 10000, seed: int = 42) -> list[dict[str, object]]:
    rng = random.Random(seed)
    rows: list[dict[str, object]] = []

    for trial in range(1, trials + 1):
        ordinary_return = rng.gauss(strategy.mean_return, strategy.volatility)
        shock = strategy.shock_size if rng.random() < strategy.shock_probability else 0.0
        simulated_return = ordinary_return + shock + strategy.recovery_credit

        rows.append({
            "trial": trial,
            "strategy": strategy.name,
            "simulated_return": round(simulated_return, 6),
            "loss": round(max(0.0, -simulated_return), 6),
            "threshold_breach": simulated_return <= -0.10,
        })

    return rows


def quantile(values: list[float], probability: float) -> float:
    if not values:
        raise ValueError("No values supplied.")
    sorted_values = sorted(values)
    index = int(probability * (len(sorted_values) - 1))
    return sorted_values[index]


def summarize_risk(rows: list[dict[str, object]], alpha: float = 0.05) -> list[dict[str, object]]:
    strategies = sorted({str(row["strategy"]) for row in rows})
    output: list[dict[str, object]] = []

    for strategy in strategies:
        subset = [row for row in rows if row["strategy"] == strategy]
        returns = [float(row["simulated_return"]) for row in subset]
        losses = [float(row["loss"]) for row in subset]
        breaches = [bool(row["threshold_breach"]) for row in subset]

        var_alpha = quantile(returns, alpha)
        tail_returns = [value for value in returns if value <= var_alpha]
        cvar_alpha = mean(tail_returns)

        expected_loss = mean(losses)
        volatility = pstdev(returns)
        downside_breach_probability = sum(1 for item in breaches if item) / len(breaches)

        risk_penalty_score = (
            expected_loss * 0.35
            + volatility * 0.20
            + abs(cvar_alpha) * 0.30
            + downside_breach_probability * 0.15
        )

        risk_adjusted_score = mean(returns) - risk_penalty_score

        output.append({
            "strategy": strategy,
            "mean_return": round(mean(returns), 6),
            "expected_loss": round(expected_loss, 6),
            "volatility": round(volatility, 6),
            "downside_breach_probability": round(downside_breach_probability, 6),
            "value_at_risk_5pct": round(var_alpha, 6),
            "conditional_value_at_risk_5pct": round(cvar_alpha, 6),
            "minimum_return": round(min(returns), 6),
            "maximum_return": round(max(returns), 6),
            "risk_penalty_score": round(risk_penalty_score, 6),
            "risk_adjusted_score": round(risk_adjusted_score, 6),
        })

    return sorted(output, key=lambda row: float(row["risk_adjusted_score"]), reverse=True)


def stress_test(strategies: list[Strategy], scenarios: list[StressScenario]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    for strategy in strategies:
        for scenario in scenarios:
            stressed_mean = strategy.mean_return + scenario.return_shift
            stressed_volatility = strategy.volatility * scenario.volatility_multiplier
            stressed_shock = strategy.shock_size * scenario.shock_multiplier

            expected_stress_return = (
                stressed_mean
                + strategy.shock_probability * stressed_shock
                + strategy.recovery_credit
            )

            rows.append({
                "strategy": strategy.name,
                "scenario": scenario.name,
                "expected_stress_return": round(expected_stress_return, 6),
                "stressed_volatility": round(stressed_volatility, 6),
                "stressed_shock": round(stressed_shock, 6),
            })

    return rows


def probability_quality_summary() -> list[dict[str, object]]:
    rows = read_csv_dicts(DATA / "synthetic_probability_estimates.csv")
    grouped: dict[str, list[float]] = {}

    for row in rows:
        grouped.setdefault(row["strategy"], []).append(QUALITY_SCORES.get(row["quality"].lower(), 0.0))

    return [
        {
            "strategy": strategy,
            "probability_quality_score": round(mean(scores), 6),
            "probability_quality_flag": "review" if mean(scores) < 0.60 else "acceptable",
        }
        for strategy, scores in sorted(grouped.items())
    ]


def expected_loss_from_hazards() -> list[dict[str, object]]:
    probabilities = read_csv_dicts(DATA / "synthetic_probability_estimates.csv")
    consequences = read_csv_dicts(DATA / "synthetic_consequences.csv")

    consequence_lookup = {
        (row["hazard_id"], row["strategy"]): float(row["loss"])
        for row in consequences
    }

    rows: list[dict[str, object]] = []
    for row in probabilities:
        key = (row["hazard_id"], row["strategy"])
        loss = consequence_lookup.get(key, 0.0)
        probability = float(row["probability"])
        rows.append({
            "hazard_id": row["hazard_id"],
            "strategy": row["strategy"],
            "probability": probability,
            "loss": loss,
            "expected_loss": round(probability * loss, 6),
            "probability_quality": row["quality"],
            "source_type": row["source_type"],
            "confidence": float(row["confidence"]),
        })

    return rows


def bayesian_update(prior: float, sensitivity: float, false_positive_rate: float) -> float:
    evidence_probability = sensitivity * prior + false_positive_rate * (1.0 - prior)
    if evidence_probability == 0:
        raise ValueError("Evidence probability is zero.")
    return (sensitivity * prior) / evidence_probability


def bayesian_update_rows() -> list[dict[str, object]]:
    cases = [
        {"case": "model drift signal", "prior": 0.10, "sensitivity": 0.82, "false_positive_rate": 0.12},
        {"case": "cost escalation alert", "prior": 0.15, "sensitivity": 0.76, "false_positive_rate": 0.18},
        {"case": "compound stress indicator", "prior": 0.06, "sensitivity": 0.70, "false_positive_rate": 0.10},
    ]

    rows = []
    for case in cases:
        posterior = bayesian_update(case["prior"], case["sensitivity"], case["false_positive_rate"])
        rows.append({
            **case,
            "posterior_after_positive_signal": round(posterior, 6),
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
    strategies = load_strategies()
    scenarios = load_scenarios()

    all_rows: list[dict[str, object]] = []
    for index, strategy in enumerate(strategies):
        all_rows.extend(simulate_strategy(strategy, trials=10000, seed=42 + index))

    summary = summarize_risk(all_rows, alpha=0.05)
    stress_rows = stress_test(strategies, scenarios)
    probability_quality = probability_quality_summary()
    hazard_expected_loss = expected_loss_from_hazards()
    bayesian_updates = bayesian_update_rows()

    write_csv(TABLES / "risk_simulation_trials.csv", all_rows)
    write_csv(TABLES / "risk_profile_summary.csv", summary)
    write_csv(TABLES / "scenario_stress_results.csv", stress_rows)
    write_csv(TABLES / "probability_quality_summary.csv", probability_quality)
    write_csv(TABLES / "hazard_expected_loss_summary.csv", hazard_expected_loss)
    write_csv(TABLES / "bayesian_risk_update_summary.csv", bayesian_updates)

    write_json(
        RECORDS / "risk_analysis_decision_record.json",
        {
            "article": "Risk Analysis and Probabilistic Reasoning",
            "decision_context": "Comparison of strategies across expected loss, volatility, tail exposure, and scenario stress.",
            "modeling_principles": [
                "Risk combines likelihood, consequence, exposure, vulnerability, and response capacity.",
                "Expected loss is useful but incomplete.",
                "Variance, threshold breach, VaR, and CVaR reveal distributional risk.",
                "Stress tests reveal exposure under severe plausible conditions.",
                "Probability assumptions and model limits should be documented.",
                "Bayesian updating can revise risk estimates as evidence changes.",
                "Risk analysis supports judgment; it does not replace responsibility.",
            ],
            "risk_summary": summary,
            "stress_results": stress_rows,
            "probability_quality": probability_quality,
            "bayesian_updates": bayesian_updates,
        },
    )

    print("Risk analysis workflow complete.")
    print(TABLES / "risk_profile_summary.csv")
    print(TABLES / "scenario_stress_results.csv")
    print(TABLES / "probability_quality_summary.csv")
    print(TABLES / "bayesian_risk_update_summary.csv")
    print(RECORDS / "risk_analysis_decision_record.json")


if __name__ == "__main__":
    main()
