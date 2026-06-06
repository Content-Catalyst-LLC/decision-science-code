#!/usr/bin/env python3
"""
Future Directions in Decision Science workflow.

Simulates future decision-system maturity across AI support, governance,
uncertainty capability, stakeholder legitimacy, reproducibility, systems awareness,
ethical accountability, adaptive capacity, failure risk, and review triggers.

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
    "Traditional Analytic Decision Support": {
        "ai_support": 0.20,
        "governance": 0.46,
        "uncertainty": 0.58,
        "legitimacy": 0.32,
        "reproducibility": 0.48,
        "systems_awareness": 0.42,
        "ethics": 0.44,
        "adaptive_capacity": 0.40,
        "failure_risk": 0.62,
        "learning_capacity": 0.46,
    },
    "AI-Enhanced Decision Support": {
        "ai_support": 0.78,
        "governance": 0.54,
        "uncertainty": 0.62,
        "legitimacy": 0.40,
        "reproducibility": 0.62,
        "systems_awareness": 0.56,
        "ethics": 0.50,
        "adaptive_capacity": 0.54,
        "failure_risk": 0.56,
        "learning_capacity": 0.58,
    },
    "Adaptive Robust Decision System": {
        "ai_support": 0.66,
        "governance": 0.78,
        "uncertainty": 0.90,
        "legitimacy": 0.66,
        "reproducibility": 0.74,
        "systems_awareness": 0.84,
        "ethics": 0.76,
        "adaptive_capacity": 0.90,
        "failure_risk": 0.30,
        "learning_capacity": 0.86,
    },
    "Integrated Future Decision Science": {
        "ai_support": 0.86,
        "governance": 0.90,
        "uncertainty": 0.88,
        "legitimacy": 0.84,
        "reproducibility": 0.88,
        "systems_awareness": 0.86,
        "ethics": 0.90,
        "adaptive_capacity": 0.88,
        "failure_risk": 0.24,
        "learning_capacity": 0.92,
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
    governance_trigger: float,
    uncertainty_trigger: float,
    ethics_trigger: float,
    adaptive_trigger: float,
    failure_risk_trigger: float,
) -> list[dict[str, object]]:
    ai_support = config["ai_support"]
    governance = config["governance"]
    uncertainty = config["uncertainty"]
    legitimacy = config["legitimacy"]
    reproducibility = config["reproducibility"]
    systems_awareness = config["systems_awareness"]
    ethics = config["ethics"]
    adaptive_capacity = config["adaptive_capacity"]
    failure_risk = config["failure_risk"]
    learning = config["learning_capacity"]
    rows: list[dict[str, object]] = []

    for time in range(1, time_steps + 1):
        disruption_event = random.random() < 0.18
        disruption = random.uniform(0.08, 0.30) if disruption_event else random.uniform(0.00, 0.05)

        ai_support = max(0.0, min(1.0, ai_support + 0.010 * learning - 0.012 * disruption + random.gauss(0.0, 0.012)))
        governance = max(0.0, min(1.0, governance + 0.012 * learning + 0.006 * reproducibility - 0.014 * disruption + random.gauss(0.0, 0.012)))
        uncertainty = max(0.0, min(1.0, uncertainty + 0.014 * learning + 0.006 * systems_awareness - 0.010 * disruption + random.gauss(0.0, 0.012)))
        reproducibility = max(0.0, min(1.0, reproducibility + 0.012 * learning + 0.006 * governance - 0.010 * disruption + random.gauss(0.0, 0.012)))
        systems_awareness = max(0.0, min(1.0, systems_awareness + 0.012 * learning + 0.006 * uncertainty - 0.012 * disruption + random.gauss(0.0, 0.012)))
        ethics = max(0.0, min(1.0, ethics + 0.010 * governance + 0.008 * legitimacy - 0.012 * disruption + random.gauss(0.0, 0.012)))
        adaptive_capacity = max(0.0, min(1.0, adaptive_capacity + 0.014 * learning + 0.008 * uncertainty - 0.014 * disruption + random.gauss(0.0, 0.012)))

        legitimacy = max(
            0.0,
            min(
                1.0,
                legitimacy
                + 0.010 * governance
                + 0.010 * ethics
                + 0.008 * reproducibility
                - 0.014 * disruption
                - 0.018 * failure_risk
                + random.gauss(0.0, 0.012),
            ),
        )

        failure_risk = max(
            0.0,
            min(
                1.0,
                failure_risk
                + 0.080 * disruption
                + 0.060 * max(0.0, governance_trigger - governance)
                + 0.060 * max(0.0, uncertainty_trigger - uncertainty)
                + 0.060 * max(0.0, ethics_trigger - ethics)
                + 0.060 * max(0.0, adaptive_trigger - adaptive_capacity)
                - 0.060 * governance
                - 0.050 * adaptive_capacity
                - 0.040 * reproducibility
                + random.gauss(0.0, 0.014),
            ),
        )

        future_decision_maturity = (
            0.12 * ai_support
            + 0.14 * governance
            + 0.14 * uncertainty
            + 0.12 * legitimacy
            + 0.12 * reproducibility
            + 0.12 * systems_awareness
            + 0.14 * ethics
            + 0.14 * adaptive_capacity
            - 0.14 * failure_risk
        )

        review_required = (
            governance <= governance_trigger
            or uncertainty <= uncertainty_trigger
            or ethics <= ethics_trigger
            or adaptive_capacity <= adaptive_trigger
            or failure_risk >= failure_risk_trigger
        )

        if review_required:
            governance = min(1.0, governance + 0.035)
            uncertainty = min(1.0, uncertainty + 0.030)
            reproducibility = min(1.0, reproducibility + 0.030)
            ethics = min(1.0, ethics + 0.035)
            adaptive_capacity = min(1.0, adaptive_capacity + 0.035)
            failure_risk = max(0.0, failure_risk - 0.045 * learning)

        rows.append({
            "decision_system": name,
            "time": time,
            "ai_support": round(ai_support, 6),
            "governance": round(governance, 6),
            "uncertainty_capability": round(uncertainty, 6),
            "stakeholder_legitimacy": round(legitimacy, 6),
            "reproducibility": round(reproducibility, 6),
            "systems_awareness": round(systems_awareness, 6),
            "ethical_accountability": round(ethics, 6),
            "adaptive_capacity": round(adaptive_capacity, 6),
            "failure_risk": round(failure_risk, 6),
            "future_decision_maturity": round(future_decision_maturity, 6),
            "disruption_event": disruption_event,
            "disruption_severity": round(disruption, 6),
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
                governance_trigger=params["governance_trigger"],
                uncertainty_trigger=params["uncertainty_trigger"],
                ethics_trigger=params["ethics_trigger"],
                adaptive_trigger=params["adaptive_trigger"],
                failure_risk_trigger=params["failure_risk_trigger"],
            )
        )

    return rows


def summarize(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    systems = sorted({str(row["decision_system"]) for row in rows})
    summary: list[dict[str, object]] = []

    for system in systems:
        system_rows = [row for row in rows if row["decision_system"] == system]
        maturity = [float(row["future_decision_maturity"]) for row in system_rows]
        governance = [float(row["governance"]) for row in system_rows]
        uncertainty = [float(row["uncertainty_capability"]) for row in system_rows]
        ethics = [float(row["ethical_accountability"]) for row in system_rows]
        adaptive = [float(row["adaptive_capacity"]) for row in system_rows]
        failure = [float(row["failure_risk"]) for row in system_rows]
        review_count = sum(1 for row in system_rows if bool(row["review_required"]))

        summary.append({
            "decision_system": system,
            "average_future_decision_maturity": round(mean(maturity), 6),
            "minimum_governance": round(min(governance), 6),
            "minimum_uncertainty_capability": round(min(uncertainty), 6),
            "minimum_ethical_accountability": round(min(ethics), 6),
            "minimum_adaptive_capacity": round(min(adaptive), 6),
            "maximum_failure_risk": round(max(failure), 6),
            "review_required_count": review_count,
            "review_flag": "review" if review_count > 0 else "acceptable",
        })

    summary.sort(key=lambda row: float(row["average_future_decision_maturity"]), reverse=True)
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

    write_csv(TABLES / "future_decision_science_timeseries.csv", rows)
    write_csv(TABLES / "future_decision_science_summary.csv", summary_rows)

    write_json(
        RECORDS / "future_decision_science_record.json",
        {
            "article": "Future Directions in Decision Science",
            "decision_context": "Simulating AI support, governance, uncertainty capability, legitimacy, reproducibility, systems awareness, ethical accountability, adaptive capacity, failure risk, and review triggers.",
            "parameters": params,
            "summary_metrics": summary_rows,
            "modeling_principles": [
                "Future decision science should integrate AI support with human judgment and institutional accountability.",
                "Decision systems should be adaptive, reproducible, participatory, and ethically accountable.",
                "Robustness and legitimacy matter alongside optimization.",
                "Review triggers should activate when governance, uncertainty capability, ethics, adaptive capacity, or failure risk crosses thresholds.",
                "Institutional learning should improve decision capacity over time."
            ],
        },
    )

    print("Future decision science simulation complete.")
    print(TABLES / "future_decision_science_timeseries.csv")
    print(TABLES / "future_decision_science_summary.csv")
    print(RECORDS / "future_decision_science_record.json")


if __name__ == "__main__":
    main()
