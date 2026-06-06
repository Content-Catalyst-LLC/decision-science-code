#!/usr/bin/env python3
"""Simulate crisis risk, uncertainty, public trust, resources, cascading impact, and escalation."""

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

CRISIS_TYPES = {
    "Infrastructure Outage": {"initial_risk": 0.48, "risk_growth": 0.026, "uncertainty": 0.46, "resource_pressure": 0.42, "public_trust": 0.66, "cascading_potential": 0.58, "response_capacity": 0.68, "adaptability": 0.72},
    "Cyber Incident": {"initial_risk": 0.52, "risk_growth": 0.030, "uncertainty": 0.58, "resource_pressure": 0.50, "public_trust": 0.62, "cascading_potential": 0.70, "response_capacity": 0.62, "adaptability": 0.66},
    "Public Health Emergency": {"initial_risk": 0.50, "risk_growth": 0.024, "uncertainty": 0.64, "resource_pressure": 0.56, "public_trust": 0.58, "cascading_potential": 0.62, "response_capacity": 0.60, "adaptability": 0.70},
    "Severe Weather Disaster": {"initial_risk": 0.56, "risk_growth": 0.034, "uncertainty": 0.50, "resource_pressure": 0.60, "public_trust": 0.60, "cascading_potential": 0.76, "response_capacity": 0.64, "adaptability": 0.74},
}


def read_params() -> dict[str, float]:
    with (DATA / "synthetic_system_parameters.csv").open("r", encoding="utf-8", newline="") as handle:
        return {row["parameter"]: float(row["value"]) for row in csv.DictReader(handle)}


def simulate_one(name: str, cfg: dict[str, float], params: dict[str, float]) -> list[dict[str, object]]:
    risk = cfg["initial_risk"]
    uncertainty = cfg["uncertainty"]
    resource_pressure = cfg["resource_pressure"]
    public_trust = cfg["public_trust"]
    cascading = cfg["cascading_potential"]
    response_capacity = cfg["response_capacity"]
    rows: list[dict[str, object]] = []

    for time in range(1, int(params["time_steps"]) + 1):
        shock_event = random.random() < 0.18
        shock = random.uniform(0.08, 0.28) if shock_event else random.uniform(0.00, 0.06)

        uncertainty = max(0.0, min(1.0, uncertainty + random.gauss(0, 0.025) + 0.08 * shock - 0.020 * cfg["adaptability"]))
        resource_pressure = max(0.0, min(1.0, resource_pressure + 0.06 * shock + 0.025 * risk - 0.020 * response_capacity + random.gauss(0, 0.020)))
        cascading = max(0.0, min(1.0, cascading + 0.07 * shock + 0.020 * risk - 0.020 * response_capacity - 0.015 * cfg["adaptability"] + random.gauss(0, 0.018)))
        public_trust = max(0.0, min(1.0, public_trust - 0.030 * shock - 0.020 * uncertainty - 0.018 * resource_pressure + 0.018 * cfg["adaptability"] + random.gauss(0, 0.018)))
        risk = max(0.0, min(1.0, risk + cfg["risk_growth"] + 0.18 * shock + 0.10 * cascading + 0.08 * uncertainty + 0.08 * resource_pressure - 0.10 * response_capacity - 0.08 * cfg["adaptability"] + random.gauss(0, 0.020)))

        escalation = (
            risk >= params["risk_trigger"]
            or uncertainty >= params["uncertainty_trigger"]
            or public_trust <= params["trust_trigger"]
            or resource_pressure >= params["resource_trigger"]
            or cascading >= params["cascading_trigger"]
        )

        if escalation:
            response_capacity = min(1.0, response_capacity + 0.06)
            risk = max(0.0, risk - 0.06 * cfg["adaptability"])
            uncertainty = max(0.0, uncertainty - 0.035 * cfg["adaptability"])
            resource_pressure = max(0.0, resource_pressure - 0.035 * response_capacity)
            public_trust = min(1.0, public_trust + 0.025)

        rows.append({
            "crisis_type": name,
            "time": time,
            "risk": round(risk, 6),
            "uncertainty": round(uncertainty, 6),
            "resource_pressure": round(resource_pressure, 6),
            "public_trust": round(public_trust, 6),
            "cascading_impact": round(cascading, 6),
            "response_capacity": round(response_capacity, 6),
            "shock_event": shock_event,
            "shock_severity": round(shock, 6),
            "escalation_required": escalation,
        })
    return rows


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    params = read_params()
    random.seed(int(params["random_seed"]))
    rows: list[dict[str, object]] = []
    for name, cfg in CRISIS_TYPES.items():
        rows.extend(simulate_one(name, cfg, params))

    summary: list[dict[str, object]] = []
    for crisis_type in sorted({str(row["crisis_type"]) for row in rows}):
        c_rows = [row for row in rows if row["crisis_type"] == crisis_type]
        risk = [float(row["risk"]) for row in c_rows]
        uncertainty = [float(row["uncertainty"]) for row in c_rows]
        trust = [float(row["public_trust"]) for row in c_rows]
        resources = [float(row["resource_pressure"]) for row in c_rows]
        cascading = [float(row["cascading_impact"]) for row in c_rows]
        summary.append({
            "crisis_type": crisis_type,
            "final_risk": round(risk[-1], 6),
            "maximum_risk": round(max(risk), 6),
            "average_risk": round(mean(risk), 6),
            "maximum_uncertainty": round(max(uncertainty), 6),
            "minimum_public_trust": round(min(trust), 6),
            "maximum_resource_pressure": round(max(resources), 6),
            "maximum_cascading_impact": round(max(cascading), 6),
            "shock_event_count": sum(1 for row in c_rows if bool(row["shock_event"])),
            "escalation_required_count": sum(1 for row in c_rows if bool(row["escalation_required"])),
        })

    write_csv(TABLES / "crisis_response_timeseries.csv", rows)
    write_csv(TABLES / "crisis_response_summary.csv", summary)

    RECORDS.mkdir(parents=True, exist_ok=True)
    (RECORDS / "crisis_management_decision_record.json").write_text(json.dumps({
        "article": "Decision Science in Crisis Management",
        "decision_context": "Simulating crisis risk, uncertainty, resource pressure, public trust, cascading impact, response capacity, and escalation triggers.",
        "parameters": params,
        "summary_metrics": summary,
        "modeling_principles": [
            "Crisis decisions should distinguish facts, assumptions, uncertainty, and decision triggers.",
            "Escalation should be connected to risk, uncertainty, resource pressure, public trust, and cascading impact.",
            "Public communication and public trust are operational variables.",
            "Adaptive response requires monitoring indicators, revision authority, and decision records.",
            "After-action review should change future plans, budgets, training, authority, and institutional learning."
        ]
    }, indent=2), encoding="utf-8")

    print(TABLES / "crisis_response_timeseries.csv")
    print(TABLES / "crisis_response_summary.csv")
    print(RECORDS / "crisis_management_decision_record.json")


if __name__ == "__main__":
    main()
