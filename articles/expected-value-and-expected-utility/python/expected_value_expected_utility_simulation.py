#!/usr/bin/env python3
"""
Expected Value and Expected Utility Simulation

Computes expected value, expected utility, certainty equivalents,
risk premiums, ranking sensitivity, and decision-record summaries.

Uses only the Python standard library.
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
class Prospect:
    name: str
    outcomes: tuple[float, ...]
    probabilities: tuple[float, ...]


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def load_prospects() -> list[Prospect]:
    rows = read_csv_dicts(DATA / "synthetic_outcomes.csv")
    grouped: dict[str, list[tuple[float, float]]] = {}

    for row in rows:
        grouped.setdefault(row["prospect"], []).append((float(row["outcome"]), float(row["probability"])))

    prospects = []
    for name, pairs in grouped.items():
        outcomes = tuple(pair[0] for pair in pairs)
        probabilities = tuple(pair[1] for pair in pairs)
        prospects.append(Prospect(name, outcomes, probabilities))

    return prospects


def validate_probabilities(prospect: Prospect) -> None:
    total = sum(prospect.probabilities)
    if not math.isclose(total, 1.0, abs_tol=1e-9):
        raise ValueError(f"Probabilities for {prospect.name} sum to {total}, not 1.")


def expected_value(prospect: Prospect) -> float:
    validate_probabilities(prospect)
    return sum(outcome * probability for outcome, probability in zip(prospect.outcomes, prospect.probabilities))


def shifted_outcome(x: float, offset: float = 151.0) -> float:
    z = x + offset
    if z <= 0:
        raise ValueError("Shifted outcome must be positive for utility calculation.")
    return z


def crra_utility(x: float, rho: float, offset: float = 151.0) -> float:
    z = shifted_outcome(x, offset)
    if math.isclose(rho, 1.0, abs_tol=1e-9):
        return math.log(z)
    return (z ** (1.0 - rho) - 1.0) / (1.0 - rho)


def inverse_crra(u: float, rho: float, offset: float = 151.0) -> float:
    if math.isclose(rho, 1.0, abs_tol=1e-9):
        return math.exp(u) - offset

    inside = u * (1.0 - rho) + 1.0
    if inside <= 0:
        return float("-inf")

    return (inside ** (1.0 / (1.0 - rho))) - offset


def expected_utility(prospect: Prospect, rho: float) -> float:
    validate_probabilities(prospect)
    return sum(
        probability * crra_utility(outcome, rho)
        for outcome, probability in zip(prospect.outcomes, prospect.probabilities)
    )


def certainty_equivalent(prospect: Prospect, rho: float) -> float:
    return inverse_crra(expected_utility(prospect, rho), rho)


def risk_premium(prospect: Prospect, rho: float) -> float:
    return expected_value(prospect) - certainty_equivalent(prospect, rho)


def rank_descending(rows: list[dict[str, object]], field: str, rank_field: str) -> None:
    sorted_rows = sorted(rows, key=lambda row: float(row[field]), reverse=True)
    rank_lookup = {id(row): rank for rank, row in enumerate(sorted_rows, start=1)}
    for row in rows:
        row[rank_field] = rank_lookup[id(row)]


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
    prospects = load_prospects()
    risk_levels = [0.25, 0.75, 1.0, 1.50, 2.25]
    rows: list[dict[str, object]] = []

    for rho in risk_levels:
        batch: list[dict[str, object]] = []

        for prospect in prospects:
            ev = expected_value(prospect)
            eu = expected_utility(prospect, rho)
            ce = certainty_equivalent(prospect, rho)
            rp = risk_premium(prospect, rho)

            batch.append({
                "risk_aversion": rho,
                "prospect": prospect.name,
                "expected_value": round(ev, 4),
                "expected_utility": round(eu, 8),
                "certainty_equivalent": round(ce, 4),
                "risk_premium": round(rp, 4),
            })

        rank_descending(batch, "expected_value", "expected_value_rank")
        rank_descending(batch, "expected_utility", "expected_utility_rank")
        rank_descending(batch, "certainty_equivalent", "certainty_equivalent_rank")
        rows.extend(batch)

    summary_rows: list[dict[str, object]] = []

    for prospect in prospects:
        prospect_rows = [row for row in rows if row["prospect"] == prospect.name]
        eu_ranks = [int(row["expected_utility_rank"]) for row in prospect_rows]
        ce_values = [float(row["certainty_equivalent"]) for row in prospect_rows]
        risk_premiums = [float(row["risk_premium"]) for row in prospect_rows]

        summary_rows.append({
            "prospect": prospect.name,
            "expected_value": round(expected_value(prospect), 4),
            "best_expected_utility_rank": min(eu_ranks),
            "worst_expected_utility_rank": max(eu_ranks),
            "rank_range": max(eu_ranks) - min(eu_ranks),
            "average_certainty_equivalent": round(mean(ce_values), 4),
            "average_risk_premium": round(mean(risk_premiums), 4),
        })

    summary_rows = sorted(summary_rows, key=lambda row: float(row["expected_value"]), reverse=True)

    write_csv(TABLES / "expected_utility_sensitivity.csv", rows)
    write_csv(TABLES / "expected_utility_summary.csv", summary_rows)

    write_json(
        RECORDS / "expected_value_expected_utility_decision_record.json",
        {
            "article": "Expected Value and Expected Utility",
            "decision_context": "Comparison of uncertain prospects under expected value and expected utility.",
            "modeling_principles": [
                "Expected value is a risk-neutral benchmark.",
                "Expected utility incorporates risk attitude through utility curvature.",
                "Certainty equivalents translate expected utility into interpretable outcome terms.",
                "Risk premiums measure willingness to give up expected value for certainty.",
                "Choice rankings can change when risk aversion changes.",
                "Probability and utility assumptions should be documented and sensitivity-tested.",
            ],
            "summary": summary_rows,
        },
    )

    print("Expected value and expected utility workflow complete.")
    print(TABLES / "expected_utility_sensitivity.csv")
    print(TABLES / "expected_utility_summary.csv")
    print(RECORDS / "expected_value_expected_utility_decision_record.json")


if __name__ == "__main__":
    main()
