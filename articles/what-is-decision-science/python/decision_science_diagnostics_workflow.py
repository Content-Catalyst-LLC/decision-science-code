#!/usr/bin/env python3
"""
Decision Science Diagnostics Workflow

Professional, dependency-light workflow for:
- expected value
- expected utility
- outcome matrix
- regret matrix
- robustness diagnostics
- multi-criteria decision analysis
- sensitivity analysis
- decision-record export

The script uses synthetic data and Python standard library only.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import csv
import json
import math
from statistics import mean

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
DATA = ARTICLE_ROOT / "data"
TABLES = ARTICLE_ROOT / "outputs" / "tables"
RECORDS = ARTICLE_ROOT / "outputs" / "decision_records"


@dataclass(frozen=True)
class Scenario:
    name: str
    probability: float
    demand_multiplier: float
    cost_pressure: float
    implementation_risk: float
    disruption_level: float


@dataclass(frozen=True)
class Alternative:
    name: str
    base_benefit: float
    base_cost: float
    flexibility: float
    resilience: float
    implementation_capacity: float
    equity_score: float
    evidence_quality: float
    reversibility: float


@dataclass(frozen=True)
class Criterion:
    name: str
    weight: float
    direction: str


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def load_scenarios() -> list[Scenario]:
    rows = read_csv_dicts(DATA / "synthetic_scenarios.csv")
    scenarios = [
        Scenario(
            name=row["scenario"],
            probability=float(row["probability"]),
            demand_multiplier=float(row["demand_multiplier"]),
            cost_pressure=float(row["cost_pressure"]),
            implementation_risk=float(row["implementation_risk"]),
            disruption_level=float(row["disruption_level"]),
        )
        for row in rows
    ]
    validate_probabilities(scenarios)
    return scenarios


def load_alternatives() -> list[Alternative]:
    rows = read_csv_dicts(DATA / "synthetic_alternatives.csv")
    return [
        Alternative(
            name=row["alternative"],
            base_benefit=float(row["base_benefit"]),
            base_cost=float(row["base_cost"]),
            flexibility=float(row["flexibility"]),
            resilience=float(row["resilience"]),
            implementation_capacity=float(row["implementation_capacity"]),
            equity_score=float(row["equity_score"]),
            evidence_quality=float(row["evidence_quality"]),
            reversibility=float(row["reversibility"]),
        )
        for row in rows
    ]


def load_criteria() -> list[Criterion]:
    rows = read_csv_dicts(DATA / "synthetic_criteria.csv")
    criteria = [
        Criterion(row["criterion"], float(row["weight"]), row["direction"])
        for row in rows
    ]
    total_weight = sum(item.weight for item in criteria)
    if not math.isclose(total_weight, 1.0, abs_tol=1e-8):
        raise ValueError(f"Criteria weights must sum to 1. Current sum: {total_weight}")
    return criteria


def validate_probabilities(scenarios: list[Scenario]) -> None:
    total_probability = sum(scenario.probability for scenario in scenarios)
    if not math.isclose(total_probability, 1.0, abs_tol=1e-8):
        raise ValueError(f"Scenario probabilities must sum to 1. Current sum: {total_probability}")


def utility(value: float, risk_aversion: float = 0.018) -> float:
    """Exponential utility for value-index outcomes."""
    return 1.0 - math.exp(-risk_aversion * value)


def scenario_outcome(alternative: Alternative, scenario: Scenario) -> float:
    benefit = alternative.base_benefit * scenario.demand_multiplier
    direct_cost = alternative.base_cost * scenario.cost_pressure
    implementation_penalty = scenario.implementation_risk * (1.0 - alternative.implementation_capacity) * 35.0
    disruption_penalty = scenario.disruption_level * (1.0 - alternative.resilience) * 45.0
    flexibility_credit = alternative.flexibility * scenario.disruption_level * 18.0
    evidence_penalty = (1.0 - alternative.evidence_quality) * 12.0
    return benefit - direct_cost - implementation_penalty - disruption_penalty + flexibility_credit - evidence_penalty


def expected_value(alternative: Alternative, scenarios: list[Scenario]) -> float:
    return sum(s.probability * scenario_outcome(alternative, s) for s in scenarios)


def expected_utility(alternative: Alternative, scenarios: list[Scenario]) -> float:
    return sum(s.probability * utility(scenario_outcome(alternative, s)) for s in scenarios)


def normalize(values: dict[str, float], direction: str) -> dict[str, float]:
    low = min(values.values())
    high = max(values.values())
    if math.isclose(high, low):
        return {key: 1.0 for key in values}
    if direction == "benefit":
        return {key: (value - low) / (high - low) for key, value in values.items()}
    if direction == "cost":
        return {key: (high - value) / (high - low) for key, value in values.items()}
    raise ValueError(f"Unknown criterion direction: {direction}")


def outcome_matrix(alternatives: list[Alternative], scenarios: list[Scenario]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for alternative in alternatives:
        for scenario in scenarios:
            rows.append({
                "alternative": alternative.name,
                "scenario": scenario.name,
                "probability": round(scenario.probability, 4),
                "outcome_value": round(scenario_outcome(alternative, scenario), 4),
            })
    return rows


def regret_matrix(alternatives: list[Alternative], scenarios: list[Scenario]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for scenario in scenarios:
        outcomes = {alternative.name: scenario_outcome(alternative, scenario) for alternative in alternatives}
        best_outcome = max(outcomes.values())
        for alternative_name, value in outcomes.items():
            rows.append({
                "alternative": alternative_name,
                "scenario": scenario.name,
                "best_scenario_outcome": round(best_outcome, 4),
                "outcome_value": round(value, 4),
                "regret": round(best_outcome - value, 4),
            })
    return rows


def mcda_scores(alternatives: list[Alternative], criteria: list[Criterion]) -> list[dict[str, object]]:
    raw: dict[str, dict[str, float]] = {
        alternative.name: {
            "net_benefit": alternative.base_benefit - alternative.base_cost,
            "flexibility": alternative.flexibility,
            "resilience": alternative.resilience,
            "implementation_capacity": alternative.implementation_capacity,
            "equity_score": alternative.equity_score,
            "evidence_quality": alternative.evidence_quality,
            "reversibility": alternative.reversibility,
        }
        for alternative in alternatives
    }

    normalized_by_criterion: dict[str, dict[str, float]] = {}
    for criterion in criteria:
        values = {name: metrics[criterion.name] for name, metrics in raw.items()}
        normalized_by_criterion[criterion.name] = normalize(values, criterion.direction)

    rows: list[dict[str, object]] = []
    for alternative in alternatives:
        score = 0.0
        for criterion in criteria:
            score += criterion.weight * normalized_by_criterion[criterion.name][alternative.name]
        rows.append({
            "alternative": alternative.name,
            "mcda_score": round(score, 4),
            "net_benefit": round(raw[alternative.name]["net_benefit"], 4),
            "flexibility": alternative.flexibility,
            "resilience": alternative.resilience,
            "implementation_capacity": alternative.implementation_capacity,
            "equity_score": alternative.equity_score,
            "evidence_quality": alternative.evidence_quality,
            "reversibility": alternative.reversibility,
        })

    return sorted(rows, key=lambda row: float(row["mcda_score"]), reverse=True)


def classify_decision_profile(expected: float, max_regret: float, robustness: float, mcda: float) -> str:
    if robustness >= 0.75 and expected >= 40.0 and max_regret <= 25.0:
        return "strong robust candidate"
    if expected >= 45.0 and max_regret > 35.0:
        return "high expected value but regret-sensitive"
    if robustness >= 0.75 and expected < 40.0:
        return "robust but moderate expected value"
    if mcda >= 0.70:
        return "strong multi-criteria profile"
    return "requires further evidence or redesign"


def summarize_decisions(
    alternatives: list[Alternative],
    scenarios: list[Scenario],
    criteria: list[Criterion],
) -> list[dict[str, object]]:
    regrets = regret_matrix(alternatives, scenarios)
    mcda = {row["alternative"]: row for row in mcda_scores(alternatives, criteria)}
    rows: list[dict[str, object]] = []

    for alternative in alternatives:
        outcomes = [scenario_outcome(alternative, scenario) for scenario in scenarios]
        alternative_regrets = [
            float(row["regret"])
            for row in regrets
            if row["alternative"] == alternative.name
        ]
        robustness_threshold = 35.0
        robustness = sum(1 for outcome in outcomes if outcome >= robustness_threshold) / len(outcomes)
        expected = expected_value(alternative, scenarios)
        max_regret = max(alternative_regrets)
        mcda_score = float(mcda[alternative.name]["mcda_score"])

        rows.append({
            "alternative": alternative.name,
            "expected_value": round(expected, 4),
            "expected_utility": round(expected_utility(alternative, scenarios), 6),
            "minimum_outcome": round(min(outcomes), 4),
            "maximum_outcome": round(max(outcomes), 4),
            "average_outcome": round(mean(outcomes), 4),
            "maximum_regret": round(max_regret, 4),
            "average_regret": round(mean(alternative_regrets), 4),
            "robustness_share": round(robustness, 4),
            "mcda_score": mcda_score,
            "evidence_quality": alternative.evidence_quality,
            "decision_note": classify_decision_profile(expected, max_regret, robustness, mcda_score),
        })

    return sorted(
        rows,
        key=lambda row: (
            float(row["robustness_share"]),
            float(row["expected_value"]),
            -float(row["maximum_regret"]),
            float(row["mcda_score"]),
        ),
        reverse=True,
    )


def sensitivity_analysis(
    alternatives: list[Alternative],
    scenarios: list[Scenario],
    criteria: list[Criterion],
) -> list[dict[str, object]]:
    base = summarize_decisions(alternatives, scenarios, criteria)
    base_top = base[0]["alternative"]
    rows: list[dict[str, object]] = []

    for criterion in criteria:
        for delta in [-0.10, 0.10]:
            revised: list[Criterion] = []
            for item in criteria:
                new_weight = item.weight + delta if item.name == criterion.name else item.weight
                revised.append(Criterion(item.name, max(0.01, new_weight), item.direction))

            total_weight = sum(item.weight for item in revised)
            revised = [
                Criterion(item.name, item.weight / total_weight, item.direction)
                for item in revised
            ]

            revised_summary = summarize_decisions(alternatives, scenarios, revised)
            revised_top = revised_summary[0]["alternative"]
            rows.append({
                "changed_criterion": criterion.name,
                "delta": delta,
                "base_top_alternative": base_top,
                "revised_top_alternative": revised_top,
                "ranking_changed": base_top != revised_top,
                "top_expected_value": revised_summary[0]["expected_value"],
                "top_maximum_regret": revised_summary[0]["maximum_regret"],
                "top_robustness_share": revised_summary[0]["robustness_share"],
                "top_mcda_score": revised_summary[0]["mcda_score"],
            })

    return rows


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"No rows to write: {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_decision_record(path: Path, summary: list[dict[str, object]], criteria: list[Criterion]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "article": "What Is Decision Science?",
        "decision": "Illustrative strategic resource-allocation decision under uncertainty",
        "selected_alternative": summary[0]["alternative"],
        "rationale": summary[0]["decision_note"],
        "modeling_principles": [
            "Define the decision before modeling options.",
            "Distinguish outcome quality from decision-process quality.",
            "Make alternatives explicit.",
            "Represent uncertainty honestly.",
            "Surface values and trade-offs.",
            "Use sensitivity analysis to test assumption dependence.",
            "Prefer robustness over fragile optimization under deep uncertainty.",
            "Document decision records for accountability and learning.",
            "Treat computational models as supports for judgment, not replacements for responsibility.",
        ],
        "criteria": [
            {"name": criterion.name, "weight": criterion.weight, "direction": criterion.direction}
            for criterion in criteria
        ],
        "summary": summary,
        "review_triggers": [
            "probability assumptions materially change",
            "maximum regret exceeds tolerance",
            "implementation capacity drops below threshold",
            "stakeholder legitimacy concerns emerge",
            "new evidence changes expected value or robustness ranking",
        ],
    }
    path.write_text(json.dumps(record, indent=2), encoding="utf-8")


def main() -> None:
    alternatives = load_alternatives()
    scenarios = load_scenarios()
    criteria = load_criteria()

    matrix = outcome_matrix(alternatives, scenarios)
    regrets = regret_matrix(alternatives, scenarios)
    mcda = mcda_scores(alternatives, criteria)
    summary = summarize_decisions(alternatives, scenarios, criteria)
    sensitivity = sensitivity_analysis(alternatives, scenarios, criteria)

    write_csv(TABLES / "decision_outcome_matrix.csv", matrix)
    write_csv(TABLES / "decision_regret_matrix.csv", regrets)
    write_csv(TABLES / "decision_mcda_scores.csv", mcda)
    write_csv(TABLES / "decision_summary.csv", summary)
    write_csv(TABLES / "decision_sensitivity_analysis.csv", sensitivity)
    write_decision_record(RECORDS / "decision_record.json", summary, criteria)

    print("Decision science workflow complete.")
    print(TABLES / "decision_summary.csv")
    print(RECORDS / "decision_record.json")


if __name__ == "__main__":
    main()
