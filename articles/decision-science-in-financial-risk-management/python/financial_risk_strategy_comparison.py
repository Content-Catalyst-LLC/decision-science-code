#!/usr/bin/env python3
"""Portfolio stress and financial risk strategy comparison workflow."""

from __future__ import annotations

from pathlib import Path
import csv
from statistics import pstdev

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
DATA = ARTICLE_ROOT / "data"
TABLES = ARTICLE_ROOT / "outputs" / "tables"


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def scenario_probabilities() -> dict[str, float]:
    return {row["scenario"]: float(row["probability"]) for row in read_csv_dicts(DATA / "synthetic_scenarios.csv")}


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"No rows to write: {path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    profiles = read_csv_dicts(DATA / "synthetic_portfolio_profiles.csv")
    probs = scenario_probabilities()
    results: list[dict[str, object]] = []

    for row in profiles:
        losses = {
            "normal": float(row["normal"]),
            "recession": float(row["recession"]),
            "liquidity_shock": float(row["liquidity_shock"]),
            "systemic_stress": float(row["systemic_stress"]),
        }

        expected_loss = sum(losses[name] * probs[name] for name in losses)
        worst_case = min(losses.values())
        regime_dispersion = pstdev(list(losses.values()))
        capital_buffer_needed = abs(worst_case) * 1.15
        liquidity_score = float(row["liquidity_score"])
        governance_score = float(row["governance_score"])
        model_confidence = float(row["model_confidence"])

        risk_resilience_score = (
            0.24 * liquidity_score
            + 0.22 * governance_score
            + 0.18 * model_confidence
            - 0.16 * abs(expected_loss) / 30.0
            - 0.14 * abs(worst_case) / 30.0
            - 0.06 * regime_dispersion / 10.0
        )

        review = (
            worst_case < -20.0
            or liquidity_score < 0.45
            or governance_score < 0.55
            or model_confidence < 0.55
            or capital_buffer_needed > 25.0
        )

        results.append({
            "portfolio": row["portfolio"],
            "expected_loss": round(expected_loss, 6),
            "worst_case": round(worst_case, 6),
            "regime_dispersion": round(regime_dispersion, 6),
            "capital_buffer_needed": round(capital_buffer_needed, 6),
            "liquidity_score": liquidity_score,
            "governance_score": governance_score,
            "model_confidence": model_confidence,
            "risk_resilience_score": round(risk_resilience_score, 6),
            "review_flag": "review" if review else "acceptable",
        })

    results = sorted(results, key=lambda item: float(item["risk_resilience_score"]), reverse=True)
    for rank, row in enumerate(results, start=1):
        row["rank"] = rank

    write_csv(TABLES / "financial_risk_regime_stress_results.csv", results)
    print(TABLES / "financial_risk_regime_stress_results.csv")


if __name__ == "__main__":
    main()
