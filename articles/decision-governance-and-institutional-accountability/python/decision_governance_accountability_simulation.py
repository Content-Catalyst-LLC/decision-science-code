#!/usr/bin/env python3
"""
Decision Governance and Institutional Accountability workflow.

Simulates accountability drift, responsibility gaps, evidence traceability,
review strength, monitoring, corrective capacity, and review triggers.

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

DECISION_SYSTEMS = {
    "Informal Approval System": {
        "accountability": 0.42,
        "decision_quality": 0.56,
        "evidence_traceability": 0.46,
        "review_strength": 0.38,
        "implementation_reliability": 0.58,
        "monitoring_strength": 0.40,
        "corrective_capacity": 0.36,
        "decision_influence": 0.72,
        "risk_pressure": 0.64,
        "learning_capacity": 0.44,
    },
    "Committee Governance System": {
        "accountability": 0.58,
        "decision_quality": 0.66,
        "evidence_traceability": 0.62,
        "review_strength": 0.64,
        "implementation_reliability": 0.62,
        "monitoring_strength": 0.54,
        "corrective_capacity": 0.52,
        "decision_influence": 0.70,
        "risk_pressure": 0.52,
        "learning_capacity": 0.58,
    },
    "Risk-Tiered Governance System": {
        "accountability": 0.76,
        "decision_quality": 0.78,
        "evidence_traceability": 0.78,
        "review_strength": 0.76,
        "implementation_reliability": 0.74,
        "monitoring_strength": 0.72,
        "corrective_capacity": 0.72,
        "decision_influence": 0.74,
        "risk_pressure": 0.42,
        "learning_capacity": 0.76,
    },
    "Adaptive Accountability System": {
        "accountability": 0.88,
        "decision_quality": 0.86,
        "evidence_traceability": 0.86,
        "review_strength": 0.88,
        "implementation_reliability": 0.84,
        "monitoring_strength": 0.90,
        "corrective_capacity": 0.92,
        "decision_influence": 0.78,
        "risk_pressure": 0.34,
        "learning_capacity": 0.90,
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
    accountability_trigger: float,
    traceability_trigger: float,
    review_trigger: float,
    responsibility_gap_trigger: float,
    risk_trigger: float,
) -> list[dict[str, object]]:
    accountability = config["accountability"]
    decision_quality = config["decision_quality"]
    traceability = config["evidence_traceability"]
    review_strength = config["review_strength"]
    implementation = config["implementation_reliability"]
    monitoring = config["monitoring_strength"]
    corrective = config["corrective_capacity"]
    risk = config["risk_pressure"]
    rows: list[dict[str, object]] = []

    for time in range(1, time_steps + 1):
        stress_event = random.random() < 0.18
        stress = random.uniform(0.08, 0.26) if stress_event else random.uniform(0.00, 0.05)

        traceability = max(0.0, min(1.0, traceability - 0.018 * stress + 0.010 * config["learning_capacity"] + random.gauss(0.0, 0.012)))
        review_strength = max(0.0, min(1.0, review_strength - 0.014 * stress + 0.012 * config["learning_capacity"] + random.gauss(0.0, 0.012)))
        monitoring = max(0.0, min(1.0, monitoring - 0.012 * stress + 0.014 * config["learning_capacity"] + random.gauss(0.0, 0.012)))
        corrective = max(0.0, min(1.0, corrective - 0.016 * stress + 0.014 * config["learning_capacity"] + random.gauss(0.0, 0.012)))
        implementation = max(0.0, min(1.0, implementation - 0.020 * stress + 0.012 * monitoring + random.gauss(0.0, 0.012)))
        decision_quality = max(0.0, min(1.0, decision_quality - 0.014 * stress + 0.014 * traceability + 0.012 * review_strength + random.gauss(0.0, 0.012)))

        accountability = max(
            0.0,
            min(
                1.0,
                accountability
                - 0.020 * stress
                + 0.015 * traceability
                + 0.015 * review_strength
                + 0.014 * monitoring
                + 0.016 * corrective
                + random.gauss(0.0, 0.012),
            ),
        )

        risk = max(
            0.0,
            min(
                1.0,
                risk
                + 0.10 * stress
                + 0.10 * max(0.0, accountability_trigger - accountability)
                + 0.08 * max(0.0, traceability_trigger - traceability)
                + 0.08 * max(0.0, review_trigger - review_strength)
                - 0.08 * monitoring
                - 0.08 * corrective
                + random.gauss(0.0, 0.014),
            ),
        )

        responsibility_gap = max(0.0, config["decision_influence"] - accountability)

        review_required = (
            accountability <= accountability_trigger
            or traceability <= traceability_trigger
            or review_strength <= review_trigger
            or responsibility_gap >= responsibility_gap_trigger
            or risk >= risk_trigger
        )

        if review_required:
            accountability = min(1.0, accountability + 0.040)
            traceability = min(1.0, traceability + 0.030)
            review_strength = min(1.0, review_strength + 0.030)
            corrective = min(1.0, corrective + 0.035)
            risk = max(0.0, risk - 0.055 * config["learning_capacity"])

        rows.append({
            "decision_system": name,
            "time": time,
            "accountability": round(accountability, 6),
            "decision_quality": round(decision_quality, 6),
            "evidence_traceability": round(traceability, 6),
            "review_strength": round(review_strength, 6),
            "implementation_reliability": round(implementation, 6),
            "monitoring_strength": round(monitoring, 6),
            "corrective_capacity": round(corrective, 6),
            "risk_exposure": round(risk, 6),
            "responsibility_gap": round(responsibility_gap, 6),
            "stress_event": stress_event,
            "stress_severity": round(stress, 6),
            "review_required": review_required,
        })

    return rows


def simulate_all() -> list[dict[str, object]]:
    params = load_parameters()
    random.seed(int(params["random_seed"]))

    rows: list[dict[str, object]] = []
    for name, config in DECISION_SYSTEMS.items():
        rows.extend(
            simulate_system(
                name,
                config,
                time_steps=int(params["time_steps"]),
                accountability_trigger=params["accountability_trigger"],
                traceability_trigger=params["traceability_trigger"],
                review_trigger=params["review_trigger"],
                responsibility_gap_trigger=params["responsibility_gap_trigger"],
                risk_trigger=params["risk_trigger"],
            )
        )

    return rows


def summarize(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    systems = sorted({str(row["decision_system"]) for row in rows})
    summary: list[dict[str, object]] = []

    for system in systems:
        system_rows = [row for row in rows if row["decision_system"] == system]
        accountability_values = [float(row["accountability"]) for row in system_rows]
        quality_values = [float(row["decision_quality"]) for row in system_rows]
        traceability_values = [float(row["evidence_traceability"]) for row in system_rows]
        review_values = [float(row["review_strength"]) for row in system_rows]
        risk_values = [float(row["risk_exposure"]) for row in system_rows]
        gap_values = [float(row["responsibility_gap"]) for row in system_rows]
        review_count = sum(1 for row in system_rows if bool(row["review_required"]))

        summary.append({
            "decision_system": system,
            "minimum_accountability": round(min(accountability_values), 6),
            "average_accountability": round(mean(accountability_values), 6),
            "average_decision_quality": round(mean(quality_values), 6),
            "minimum_evidence_traceability": round(min(traceability_values), 6),
            "minimum_review_strength": round(min(review_values), 6),
            "maximum_risk_exposure": round(max(risk_values), 6),
            "maximum_responsibility_gap": round(max(gap_values), 6),
            "review_required_count": review_count,
            "review_flag": "review" if review_count > 0 else "acceptable",
        })

    summary.sort(key=lambda row: (float(row["average_accountability"]), -float(row["maximum_risk_exposure"])), reverse=True)
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

    write_csv(TABLES / "decision_governance_timeseries.csv", rows)
    write_csv(TABLES / "decision_governance_summary.csv", summary_rows)

    write_json(
        RECORDS / "decision_governance_record.json",
        {
            "article": "Decision Governance and Institutional Accountability",
            "decision_context": "Simulating accountability drift, responsibility gaps, evidence traceability, review strength, monitoring, corrective capacity, and review triggers.",
            "parameters": params,
            "summary_metrics": summary_rows,
            "modeling_principles": [
                "Decision governance should make authority, evidence, review, implementation, monitoring, and correction explicit.",
                "Responsibility gaps appear when actors have influence without accountability.",
                "Decision records preserve institutional memory and make review possible.",
                "Risk-tiered governance should match process burden to decision consequence.",
                "Accountability requires learning loops that change future decision practice."
            ],
        },
    )

    print("Decision governance and institutional accountability simulation complete.")
    print(TABLES / "decision_governance_timeseries.csv")
    print(TABLES / "decision_governance_summary.csv")
    print(RECORDS / "decision_governance_record.json")


if __name__ == "__main__":
    main()
