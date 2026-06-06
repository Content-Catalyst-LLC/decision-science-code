#!/usr/bin/env python3
"""
Decision Science in AI Governance workflow.

Simulates AI governance review cycles under drift, incidents,
oversight limits, equity performance, security readiness, and risk escalation.

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

SYSTEMS = {
    "Internal Document Assistant": {
        "initial_risk": 0.24,
        "drift_rate": 0.012,
        "incident_probability": 0.05,
        "oversight_strength": 0.78,
        "security_readiness": 0.74,
        "equity_performance": 0.78,
        "adaptability": 0.82,
    },
    "Customer Support Generator": {
        "initial_risk": 0.36,
        "drift_rate": 0.018,
        "incident_probability": 0.08,
        "oversight_strength": 0.66,
        "security_readiness": 0.68,
        "equity_performance": 0.70,
        "adaptability": 0.72,
    },
    "Hiring Screening Model": {
        "initial_risk": 0.52,
        "drift_rate": 0.022,
        "incident_probability": 0.10,
        "oversight_strength": 0.58,
        "security_readiness": 0.64,
        "equity_performance": 0.56,
        "adaptability": 0.62,
    },
    "Clinical Decision Support": {
        "initial_risk": 0.60,
        "drift_rate": 0.016,
        "incident_probability": 0.09,
        "oversight_strength": 0.74,
        "security_readiness": 0.70,
        "equity_performance": 0.68,
        "adaptability": 0.66,
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


def simulate_system(
    name: str,
    config: dict[str, float],
    time_steps: int,
    risk_trigger: float,
    drift_trigger: float,
    equity_trigger: float,
    oversight_trigger: float,
) -> list[dict[str, object]]:
    risk = config["initial_risk"]
    drift = 0.0
    equity = config["equity_performance"]
    oversight = config["oversight_strength"]
    rows: list[dict[str, object]] = []

    for time in range(1, time_steps + 1):
        incident = random.random() < config["incident_probability"]
        incident_severity = random.uniform(0.08, 0.30) if incident else 0.0

        drift = max(
            0.0,
            min(
                1.0,
                drift
                + config["drift_rate"]
                + random.gauss(0.0, 0.015)
                - 0.012 * config["adaptability"],
            ),
        )

        equity = max(
            0.0,
            min(
                1.0,
                equity
                - 0.025 * incident_severity
                - 0.010 * drift
                + 0.006 * config["adaptability"]
                + random.gauss(0.0, 0.01),
            ),
        )

        oversight = max(
            0.0,
            min(
                1.0,
                oversight
                - 0.012 * incident_severity
                + 0.004 * config["adaptability"]
                + random.gauss(0.0, 0.008),
            ),
        )

        risk = max(
            0.0,
            min(
                1.0,
                risk
                + 0.22 * drift
                + 0.18 * incident_severity
                + 0.16 * max(0.0, equity_trigger - equity)
                + 0.12 * max(0.0, oversight_trigger - oversight)
                - 0.08 * config["security_readiness"]
                - 0.06 * config["adaptability"]
                + random.gauss(0.0, 0.015),
            ),
        )

        review_required = (
            risk >= risk_trigger
            or drift >= drift_trigger
            or equity <= equity_trigger
            or oversight <= oversight_trigger
        )

        if review_required:
            risk = max(0.0, risk - 0.08 * config["adaptability"])
            oversight = min(1.0, oversight + 0.04)
            equity = min(1.0, equity + 0.025)

        rows.append({
            "system": name,
            "time": time,
            "risk": round(risk, 6),
            "drift": round(drift, 6),
            "equity_performance": round(equity, 6),
            "oversight_strength": round(oversight, 6),
            "incident": incident,
            "incident_severity": round(incident_severity, 6),
            "review_required": review_required,
        })

    return rows


def simulate_all() -> list[dict[str, object]]:
    params = load_parameters()
    random.seed(int(params["random_seed"]))

    rows: list[dict[str, object]] = []
    for name, config in SYSTEMS.items():
        rows.extend(
            simulate_system(
                name,
                config,
                time_steps=int(params["time_steps"]),
                risk_trigger=params["risk_trigger"],
                drift_trigger=params["drift_trigger"],
                equity_trigger=params["equity_trigger"],
                oversight_trigger=params["oversight_trigger"],
            )
        )

    return rows


def summarize(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    systems = sorted({str(row["system"]) for row in rows})
    summary: list[dict[str, object]] = []

    for system in systems:
        system_rows = [row for row in rows if row["system"] == system]
        risk_values = [float(row["risk"]) for row in system_rows]
        drift_values = [float(row["drift"]) for row in system_rows]
        equity_values = [float(row["equity_performance"]) for row in system_rows]
        oversight_values = [float(row["oversight_strength"]) for row in system_rows]
        incident_count = sum(1 for row in system_rows if bool(row["incident"]))
        review_count = sum(1 for row in system_rows if bool(row["review_required"]))

        summary.append({
            "system": system,
            "final_risk": round(risk_values[-1], 6),
            "maximum_risk": round(max(risk_values), 6),
            "average_risk": round(mean(risk_values), 6),
            "maximum_drift": round(max(drift_values), 6),
            "minimum_equity_performance": round(min(equity_values), 6),
            "minimum_oversight_strength": round(min(oversight_values), 6),
            "incident_count": incident_count,
            "review_required_count": review_count,
            "review_flag": "review" if review_count > 0 else "acceptable",
        })

    summary.sort(key=lambda row: (float(row["maximum_risk"]), float(row["maximum_drift"])))
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

    write_csv(TABLES / "ai_governance_timeseries.csv", rows)
    write_csv(TABLES / "ai_governance_summary.csv", summary_rows)

    write_json(
        RECORDS / "ai_governance_decision_record.json",
        {
            "article": "Decision Science in AI Governance",
            "decision_context": "Simulating AI governance review cycles under drift, incidents, oversight limits, equity performance, and risk escalation.",
            "parameters": params,
            "summary_metrics": summary_rows,
            "modeling_principles": [
                "AI governance should evaluate use context, risk, evidence, oversight, equity, security, and accountability together.",
                "Model drift and incident patterns should trigger governance review before harm becomes institutionalized.",
                "Human oversight must be meaningful: authority, information, time, expertise, and independence are required.",
                "High-stakes AI systems require stronger evidence, monitoring, documentation, and contestability.",
                "Decision records should preserve assumptions, alternatives, risk classification, evidence, dissent, approvals, and revision triggers."
            ],
        },
    )

    print("Decision science in AI governance simulation complete.")
    print(TABLES / "ai_governance_timeseries.csv")
    print(TABLES / "ai_governance_summary.csv")
    print(RECORDS / "ai_governance_decision_record.json")


if __name__ == "__main__":
    main()
