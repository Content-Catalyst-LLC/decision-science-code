#!/usr/bin/env python3
"""
Decision Science in Financial Risk Management workflow.

Simulates capital resilience, liquidity pressure, tail shocks,
adaptive response, and decision-record export.

Uses only the Python standard library.
"""

from __future__ import annotations

from pathlib import Path
import csv
import json
import random
from statistics import mean

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
DATA = ARTICLE_ROOT / "data"
TABLES = ARTICLE_ROOT / "outputs" / "tables"
RECORDS = ARTICLE_ROOT / "outputs" / "decision_records"

PORTFOLIOS = {
    "Conservative Credit Book": {
        "initial_capital": 100.0,
        "base_return": 0.55,
        "shock_volatility": 1.2,
        "tail_probability": 0.08,
        "tail_loss_min": -6.0,
        "tail_loss_max": -3.0,
        "resilience_capacity": 1.60,
        "liquidity_drag": 0.30,
        "initial_liquidity": 0.82,
    },
    "Balanced Multi-Asset": {
        "initial_capital": 100.0,
        "base_return": 0.75,
        "shock_volatility": 1.8,
        "tail_probability": 0.10,
        "tail_loss_min": -8.0,
        "tail_loss_max": -3.5,
        "resilience_capacity": 1.30,
        "liquidity_drag": 0.50,
        "initial_liquidity": 0.68,
    },
    "Yield-Seeking Portfolio": {
        "initial_capital": 100.0,
        "base_return": 1.05,
        "shock_volatility": 2.8,
        "tail_probability": 0.14,
        "tail_loss_min": -11.0,
        "tail_loss_max": -4.0,
        "resilience_capacity": 0.80,
        "liquidity_drag": 0.80,
        "initial_liquidity": 0.48,
    },
    "Concentrated Risk Book": {
        "initial_capital": 100.0,
        "base_return": 1.20,
        "shock_volatility": 3.4,
        "tail_probability": 0.18,
        "tail_loss_min": -14.0,
        "tail_loss_max": -5.0,
        "resilience_capacity": 0.60,
        "liquidity_drag": 1.00,
        "initial_liquidity": 0.36,
    },
}


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def load_parameters() -> dict[str, float]:
    return {
        row["parameter"]: float(row["value"])
        for row in read_csv_dicts(DATA / "synthetic_system_parameters.csv")
    }


def simulate_portfolio(
    name: str,
    config: dict[str, float],
    time_steps: int,
    capital_trigger: float,
    liquidity_trigger: float,
) -> list[dict[str, object]]:
    capital = config["initial_capital"]
    liquidity = config["initial_liquidity"]
    rows: list[dict[str, object]] = []

    for time in range(1, time_steps + 1):
        ordinary_shock = random.gauss(0.0, config["shock_volatility"])
        tail_event = random.random() < config["tail_probability"]
        tail_loss = random.uniform(config["tail_loss_min"], config["tail_loss_max"]) if tail_event else 0.0

        adaptive_offset = config["resilience_capacity"] * random.uniform(0.60, 1.20)
        liquidity_drag = config["liquidity_drag"] * (1.0 + max(0.0, 0.60 - liquidity))

        period_return = (
            config["base_return"]
            + ordinary_shock
            + tail_loss
            + adaptive_offset
            - liquidity_drag
        )

        capital = max(20.0, capital * (1.0 + period_return / 100.0))

        liquidity_change = (
            -0.015
            - 0.004 * abs(tail_loss)
            - 0.003 * max(0.0, -ordinary_shock)
            + 0.006 * config["resilience_capacity"]
        )

        liquidity = max(0.05, min(1.0, liquidity + liquidity_change))

        capital_trigger_hit = capital < capital_trigger
        liquidity_trigger_hit = liquidity < liquidity_trigger
        review_required = capital_trigger_hit or liquidity_trigger_hit

        rows.append({
            "portfolio": name,
            "time": time,
            "capital": round(capital, 6),
            "liquidity": round(liquidity, 6),
            "ordinary_shock": round(ordinary_shock, 6),
            "tail_event": tail_event,
            "tail_loss": round(tail_loss, 6),
            "period_return": round(period_return, 6),
            "capital_trigger_hit": capital_trigger_hit,
            "liquidity_trigger_hit": liquidity_trigger_hit,
            "review_required": review_required,
        })

    return rows


def simulate_all() -> list[dict[str, object]]:
    params = load_parameters()
    random.seed(int(params["random_seed"]))
    rows: list[dict[str, object]] = []

    for name, config in PORTFOLIOS.items():
        rows.extend(
            simulate_portfolio(
                name,
                config,
                time_steps=int(params["time_steps"]),
                capital_trigger=params["capital_trigger"],
                liquidity_trigger=params["liquidity_trigger"],
            )
        )

    return rows


def summarize(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    portfolios = sorted({str(row["portfolio"]) for row in rows})
    summary: list[dict[str, object]] = []

    for portfolio in portfolios:
        p_rows = [row for row in rows if row["portfolio"] == portfolio]
        capital_values = [float(row["capital"]) for row in p_rows]
        liquidity_values = [float(row["liquidity"]) for row in p_rows]
        tail_count = sum(1 for row in p_rows if bool(row["tail_event"]))
        review_count = sum(1 for row in p_rows if bool(row["review_required"]))

        summary.append({
            "portfolio": portfolio,
            "final_capital": round(capital_values[-1], 6),
            "minimum_capital": round(min(capital_values), 6),
            "average_capital": round(mean(capital_values), 6),
            "final_liquidity": round(liquidity_values[-1], 6),
            "minimum_liquidity": round(min(liquidity_values), 6),
            "tail_event_count": tail_count,
            "review_required_count": review_count,
            "review_flag": "review" if review_count > 0 else "acceptable",
        })

    return summary


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
    params = load_parameters()
    rows = simulate_all()
    summary_rows = summarize(rows)

    write_csv(TABLES / "financial_risk_capital_timeseries.csv", rows)
    write_csv(TABLES / "financial_risk_capital_summary.csv", summary_rows)

    write_json(
        RECORDS / "financial_risk_decision_record.json",
        {
            "article": "Decision Science in Financial Risk Management",
            "decision_context": "Simulating capital resilience, liquidity pressure, and review triggers under tail shocks.",
            "parameters": params,
            "summary_metrics": summary_rows,
            "modeling_principles": [
                "Financial risk decisions require capital, liquidity, model, behavioral, and governance review.",
                "Tail events can change the decision problem faster than ordinary volatility metrics imply.",
                "Liquidity drag can turn mark-to-market losses into survivability problems.",
                "Review triggers should be connected to real decision authority.",
                "Decision records should preserve assumptions, overlays, stress results, dissent, and revision triggers."
            ],
        },
    )

    print("Decision science in financial risk management simulation complete.")
    print(TABLES / "financial_risk_capital_timeseries.csv")
    print(TABLES / "financial_risk_capital_summary.csv")
    print(RECORDS / "financial_risk_decision_record.json")


if __name__ == "__main__":
    main()
