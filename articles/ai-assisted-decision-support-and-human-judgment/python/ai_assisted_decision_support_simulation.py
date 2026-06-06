#!/usr/bin/env python3
"""
AI-Assisted Decision Support and Human Judgment workflow.

Simulates model confidence, model uncertainty, human oversight,
automation-bias risk, contestability, fairness risk, accountability,
monitoring, and review triggers.

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

AI_SUPPORT_SYSTEMS = {
    "Evidence Assistant": {
        "model_confidence": 0.64,
        "model_uncertainty": 0.38,
        "human_oversight": 0.84,
        "automation_bias": 0.24,
        "contestability": 0.72,
        "fairness_risk": 0.36,
        "accountability": 0.76,
        "monitoring": 0.64,
        "learning_capacity": 0.72,
    },
    "Recommendation with Review": {
        "model_confidence": 0.76,
        "model_uncertainty": 0.44,
        "human_oversight": 0.72,
        "automation_bias": 0.46,
        "contestability": 0.66,
        "fairness_risk": 0.42,
        "accountability": 0.70,
        "monitoring": 0.70,
        "learning_capacity": 0.70,
    },
    "Automated Decision with Monitoring": {
        "model_confidence": 0.84,
        "model_uncertainty": 0.50,
        "human_oversight": 0.36,
        "automation_bias": 0.72,
        "contestability": 0.40,
        "fairness_risk": 0.58,
        "accountability": 0.44,
        "monitoring": 0.70,
        "learning_capacity": 0.56,
    },
    "Adaptive Human-AI Governance": {
        "model_confidence": 0.82,
        "model_uncertainty": 0.34,
        "human_oversight": 0.88,
        "automation_bias": 0.28,
        "contestability": 0.86,
        "fairness_risk": 0.30,
        "accountability": 0.90,
        "monitoring": 0.90,
        "learning_capacity": 0.88,
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
    uncertainty_trigger: float,
    oversight_trigger: float,
    automation_bias_trigger: float,
    contestability_trigger: float,
    fairness_risk_trigger: float,
    accountability_trigger: float,
) -> list[dict[str, object]]:
    confidence = config["model_confidence"]
    uncertainty = config["model_uncertainty"]
    oversight = config["human_oversight"]
    automation_bias = config["automation_bias"]
    contestability = config["contestability"]
    fairness_risk = config["fairness_risk"]
    accountability = config["accountability"]
    monitoring = config["monitoring"]
    rows: list[dict[str, object]] = []

    for time in range(1, time_steps + 1):
        shift_event = random.random() < 0.18
        shift = random.uniform(0.08, 0.28) if shift_event else random.uniform(0.00, 0.05)

        uncertainty = max(0.0, min(1.0, uncertainty + 0.080 * shift - 0.022 * monitoring + random.gauss(0.0, 0.016)))
        confidence = max(0.0, min(1.0, confidence - 0.060 * shift + 0.020 * config["learning_capacity"] - 0.030 * uncertainty + random.gauss(0.0, 0.016)))
        oversight = max(0.0, min(1.0, oversight - 0.020 * shift + 0.012 * accountability + random.gauss(0.0, 0.014)))

        automation_bias = max(
            0.0,
            min(
                1.0,
                automation_bias
                + 0.050 * confidence
                + 0.050 * shift
                - 0.050 * oversight
                - 0.025 * uncertainty
                + random.gauss(0.0, 0.016),
            ),
        )

        contestability = max(0.0, min(1.0, contestability - 0.012 * shift + 0.014 * accountability + random.gauss(0.0, 0.014)))

        fairness_risk = max(
            0.0,
            min(
                1.0,
                fairness_risk
                + 0.060 * shift
                + 0.040 * uncertainty
                - 0.030 * monitoring
                - 0.020 * contestability
                + random.gauss(0.0, 0.016),
            ),
        )

        accountability = max(
            0.0,
            min(
                1.0,
                accountability
                - 0.020 * shift
                + 0.014 * oversight
                + 0.014 * contestability
                + 0.014 * monitoring
                + random.gauss(0.0, 0.014),
            ),
        )

        review_required = (
            uncertainty >= uncertainty_trigger
            or oversight <= oversight_trigger
            or automation_bias >= automation_bias_trigger
            or contestability <= contestability_trigger
            or fairness_risk >= fairness_risk_trigger
            or accountability <= accountability_trigger
        )

        if review_required:
            oversight = min(1.0, oversight + 0.045)
            contestability = min(1.0, contestability + 0.035)
            accountability = min(1.0, accountability + 0.040)
            automation_bias = max(0.0, automation_bias - 0.045 * config["learning_capacity"])
            fairness_risk = max(0.0, fairness_risk - 0.035 * config["learning_capacity"])

        rows.append({
            "ai_support_system": name,
            "time": time,
            "model_confidence": round(confidence, 6),
            "model_uncertainty": round(uncertainty, 6),
            "human_oversight": round(oversight, 6),
            "automation_bias": round(automation_bias, 6),
            "contestability": round(contestability, 6),
            "fairness_risk": round(fairness_risk, 6),
            "accountability": round(accountability, 6),
            "monitoring": round(monitoring, 6),
            "shift_event": shift_event,
            "shift_severity": round(shift, 6),
            "review_required": review_required,
        })

    return rows


def simulate_all() -> list[dict[str, object]]:
    params = load_parameters()
    random.seed(int(params["random_seed"]))

    rows: list[dict[str, object]] = []
    for name, config in AI_SUPPORT_SYSTEMS.items():
        rows.extend(
            simulate_system(
                name,
                config,
                time_steps=int(params["time_steps"]),
                uncertainty_trigger=params["uncertainty_trigger"],
                oversight_trigger=params["oversight_trigger"],
                automation_bias_trigger=params["automation_bias_trigger"],
                contestability_trigger=params["contestability_trigger"],
                fairness_risk_trigger=params["fairness_risk_trigger"],
                accountability_trigger=params["accountability_trigger"],
            )
        )

    return rows


def summarize(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    systems = sorted({str(row["ai_support_system"]) for row in rows})
    summary: list[dict[str, object]] = []

    for system in systems:
        system_rows = [row for row in rows if row["ai_support_system"] == system]
        uncertainty_values = [float(row["model_uncertainty"]) for row in system_rows]
        oversight_values = [float(row["human_oversight"]) for row in system_rows]
        bias_values = [float(row["automation_bias"]) for row in system_rows]
        contestability_values = [float(row["contestability"]) for row in system_rows]
        fairness_values = [float(row["fairness_risk"]) for row in system_rows]
        accountability_values = [float(row["accountability"]) for row in system_rows]
        review_count = sum(1 for row in system_rows if bool(row["review_required"]))

        summary.append({
            "ai_support_system": system,
            "maximum_model_uncertainty": round(max(uncertainty_values), 6),
            "minimum_human_oversight": round(min(oversight_values), 6),
            "maximum_automation_bias": round(max(bias_values), 6),
            "minimum_contestability": round(min(contestability_values), 6),
            "maximum_fairness_risk": round(max(fairness_values), 6),
            "minimum_accountability": round(min(accountability_values), 6),
            "average_accountability": round(mean(accountability_values), 6),
            "review_required_count": review_count,
            "review_flag": "review" if review_count > 0 else "acceptable",
        })

    summary.sort(key=lambda row: (float(row["average_accountability"]), -float(row["maximum_automation_bias"])), reverse=True)
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

    write_csv(TABLES / "ai_decision_support_timeseries.csv", rows)
    write_csv(TABLES / "ai_decision_support_summary.csv", summary_rows)

    write_json(
        RECORDS / "ai_decision_support_record.json",
        {
            "article": "AI-Assisted Decision Support and Human Judgment",
            "decision_context": "Simulating model uncertainty, human oversight, automation bias, contestability, fairness risk, accountability, and review triggers.",
            "parameters": params,
            "summary_metrics": summary_rows,
            "modeling_principles": [
                "AI should support decision quality, not replace accountable judgment.",
                "Human oversight is meaningful only when humans have authority, information, time, training, and institutional support.",
                "Model uncertainty, automation bias, fairness risk, and contestability should be monitored over time.",
                "Decision records should preserve how AI outputs influenced human decisions.",
                "Review triggers should activate when uncertainty, bias, weak oversight, fairness risk, or accountability weakness crosses thresholds."
            ],
        },
    )

    print("AI-assisted decision support simulation complete.")
    print(TABLES / "ai_decision_support_timeseries.csv")
    print(TABLES / "ai_decision_support_summary.csv")
    print(RECORDS / "ai_decision_support_record.json")


if __name__ == "__main__":
    main()
