#!/usr/bin/env python3
"""
Decision Science in Infrastructure Planning workflow.

Simulates asset condition, maintenance, hazard shocks, service reliability,
adaptation response, and decision-record export.

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

ASSETS = {
    "Aging Bridge Corridor": {
        "initial_condition": 74.0,
        "deterioration_rate": 1.15,
        "maintenance_effect": 1.25,
        "hazard_exposure": 0.62,
        "criticality": 0.84,
        "adaptability": 0.48,
    },
    "Water Distribution Network": {
        "initial_condition": 68.0,
        "deterioration_rate": 1.35,
        "maintenance_effect": 1.45,
        "hazard_exposure": 0.58,
        "criticality": 0.90,
        "adaptability": 0.62,
    },
    "Grid Modernization Package": {
        "initial_condition": 72.0,
        "deterioration_rate": 0.95,
        "maintenance_effect": 1.10,
        "hazard_exposure": 0.68,
        "criticality": 0.92,
        "adaptability": 0.78,
    },
    "Nature-Based Flood System": {
        "initial_condition": 76.0,
        "deterioration_rate": 0.70,
        "maintenance_effect": 0.95,
        "hazard_exposure": 0.74,
        "criticality": 0.76,
        "adaptability": 0.86,
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


def simulate_asset(
    name: str,
    config: dict[str, float],
    time_steps: int,
    condition_trigger: float,
    service_trigger: float,
    hazard_trigger: float,
) -> list[dict[str, object]]:
    condition = config["initial_condition"]
    adaptation_capacity = 8.0 + 8.0 * config["adaptability"]
    maintenance_level = 5.0
    rows: list[dict[str, object]] = []

    for time in range(1, time_steps + 1):
        hazard_event = random.random() < (0.08 + 0.08 * config["hazard_exposure"])
        hazard_intensity = random.uniform(0.20, 1.00) if hazard_event else random.uniform(0.00, 0.25)

        deterioration = (
            config["deterioration_rate"]
            + random.gauss(0.0, 0.30)
            + 1.80 * hazard_intensity * config["hazard_exposure"]
        )

        maintenance_gain = (
            config["maintenance_effect"] * maintenance_level / 5.0
            + 0.30 * adaptation_capacity / 10.0
        )

        condition = max(20.0, min(100.0, condition - deterioration + maintenance_gain))

        service_reliability = max(
            0.0,
            min(
                1.0,
                0.35
                + 0.0065 * condition
                + 0.10 * config["adaptability"]
                - 0.18 * hazard_intensity * config["criticality"]
            )
        )

        risk_index = max(
            0.0,
            min(
                1.0,
                0.40 * (1.0 - condition / 100.0)
                + 0.35 * config["hazard_exposure"]
                + 0.25 * config["criticality"]
                - 0.10 * config["adaptability"]
            )
        )

        review_required = (
            condition < condition_trigger
            or service_reliability < service_trigger
            or risk_index > hazard_trigger
        )

        if review_required:
            maintenance_level = min(10.0, maintenance_level + 0.75)
            adaptation_capacity = min(25.0, adaptation_capacity + 0.60)
        else:
            maintenance_level = max(4.0, maintenance_level - 0.10)

        rows.append({
            "asset": name,
            "time": time,
            "condition": round(condition, 6),
            "hazard_event": hazard_event,
            "hazard_intensity": round(hazard_intensity, 6),
            "maintenance_level": round(maintenance_level, 6),
            "adaptation_capacity": round(adaptation_capacity, 6),
            "service_reliability": round(service_reliability, 6),
            "risk_index": round(risk_index, 6),
            "review_required": review_required,
        })

    return rows


def simulate_all() -> list[dict[str, object]]:
    params = load_parameters()
    random.seed(int(params["random_seed"]))

    rows: list[dict[str, object]] = []
    for name, config in ASSETS.items():
        rows.extend(
            simulate_asset(
                name,
                config,
                time_steps=int(params["time_steps"]),
                condition_trigger=params["condition_trigger"],
                service_trigger=params["service_trigger"],
                hazard_trigger=params["hazard_trigger"],
            )
        )

    return rows


def summarize(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    assets = sorted({str(row["asset"]) for row in rows})
    summary: list[dict[str, object]] = []

    for asset in assets:
        asset_rows = [row for row in rows if row["asset"] == asset]
        condition_values = [float(row["condition"]) for row in asset_rows]
        service_values = [float(row["service_reliability"]) for row in asset_rows]
        risk_values = [float(row["risk_index"]) for row in asset_rows]
        review_count = sum(1 for row in asset_rows if bool(row["review_required"]))
        hazard_count = sum(1 for row in asset_rows if bool(row["hazard_event"]))

        summary.append({
            "asset": asset,
            "final_condition": round(condition_values[-1], 6),
            "minimum_condition": round(min(condition_values), 6),
            "average_condition": round(mean(condition_values), 6),
            "minimum_service_reliability": round(min(service_values), 6),
            "average_service_reliability": round(mean(service_values), 6),
            "maximum_risk_index": round(max(risk_values), 6),
            "average_risk_index": round(mean(risk_values), 6),
            "hazard_event_count": hazard_count,
            "review_required_count": review_count,
            "review_flag": "review" if review_count > 0 else "acceptable",
        })

    summary.sort(key=lambda row: (float(row["minimum_service_reliability"]), -float(row["maximum_risk_index"])), reverse=True)
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

    write_csv(TABLES / "infrastructure_asset_timeseries.csv", rows)
    write_csv(TABLES / "infrastructure_asset_summary.csv", summary_rows)

    write_json(
        RECORDS / "infrastructure_decision_record.json",
        {
            "article": "Decision Science in Infrastructure Planning",
            "decision_context": "Simulating asset condition, hazard shocks, maintenance response, service reliability, and adaptive review triggers.",
            "parameters": params,
            "summary_metrics": summary_rows,
            "modeling_principles": [
                "Infrastructure decisions should be evaluated across lifecycle value, service continuity, resilience, equity, and adaptability.",
                "Asset condition is not the only measure; service reliability and system criticality matter.",
                "Hazard shocks can reveal vulnerabilities that ordinary condition scores miss.",
                "Adaptive triggers should connect monitoring indicators to funding and governance authority.",
                "Decision records should preserve assumptions, alternatives, risks, trade-offs, equity concerns, and revision triggers."
            ],
        },
    )

    print("Decision science in infrastructure planning simulation complete.")
    print(TABLES / "infrastructure_asset_timeseries.csv")
    print(TABLES / "infrastructure_asset_summary.csv")
    print(RECORDS / "infrastructure_decision_record.json")


if __name__ == "__main__":
    main()
