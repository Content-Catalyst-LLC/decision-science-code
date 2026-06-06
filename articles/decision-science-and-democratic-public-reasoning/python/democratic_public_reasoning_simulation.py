#!/usr/bin/env python3
"""
Decision Science and Democratic Public Reasoning workflow.

Simulates public trust, legitimacy, participation, evidence transparency,
contestability, equity review, uncertainty communication, public harm signals,
and review triggers.

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

PUBLIC_DECISION_SYSTEMS = {
    "Internal Expert Decision": {
        "public_trust": 0.54,
        "legitimacy": 0.48,
        "participation": 0.22,
        "evidence_transparency": 0.44,
        "contestability": 0.36,
        "equity_review": 0.48,
        "uncertainty_communication": 0.52,
        "public_harm_signal": 0.48,
        "responsiveness": 0.42,
    },
    "Public Comment Process": {
        "public_trust": 0.58,
        "legitimacy": 0.60,
        "participation": 0.58,
        "evidence_transparency": 0.68,
        "contestability": 0.64,
        "equity_review": 0.56,
        "uncertainty_communication": 0.58,
        "public_harm_signal": 0.42,
        "responsiveness": 0.58,
    },
    "Deliberative Citizens Panel": {
        "public_trust": 0.68,
        "legitimacy": 0.78,
        "participation": 0.82,
        "evidence_transparency": 0.82,
        "contestability": 0.78,
        "equity_review": 0.76,
        "uncertainty_communication": 0.78,
        "public_harm_signal": 0.34,
        "responsiveness": 0.76,
    },
    "Adaptive Public Reasoning System": {
        "public_trust": 0.76,
        "legitimacy": 0.86,
        "participation": 0.88,
        "evidence_transparency": 0.88,
        "contestability": 0.86,
        "equity_review": 0.86,
        "uncertainty_communication": 0.86,
        "public_harm_signal": 0.28,
        "responsiveness": 0.88,
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
    trust_trigger: float,
    legitimacy_trigger: float,
    contestability_trigger: float,
    equity_trigger: float,
    harm_trigger: float,
) -> list[dict[str, object]]:
    trust = config["public_trust"]
    legitimacy = config["legitimacy"]
    participation = config["participation"]
    transparency = config["evidence_transparency"]
    contestability = config["contestability"]
    equity = config["equity_review"]
    uncertainty = config["uncertainty_communication"]
    harm = config["public_harm_signal"]
    responsiveness = config["responsiveness"]
    rows: list[dict[str, object]] = []

    for time in range(1, time_steps + 1):
        controversy_event = random.random() < 0.18
        controversy = random.uniform(0.08, 0.28) if controversy_event else random.uniform(0.00, 0.05)

        transparency = max(0.0, min(1.0, transparency - 0.010 * controversy + 0.012 * responsiveness + random.gauss(0.0, 0.014)))
        participation = max(0.0, min(1.0, participation - 0.012 * controversy + 0.010 * responsiveness + random.gauss(0.0, 0.014)))
        contestability = max(0.0, min(1.0, contestability - 0.014 * controversy + 0.012 * transparency + random.gauss(0.0, 0.014)))
        equity = max(0.0, min(1.0, equity - 0.012 * controversy + 0.010 * participation + 0.008 * contestability + random.gauss(0.0, 0.014)))
        uncertainty = max(0.0, min(1.0, uncertainty - 0.012 * controversy + 0.012 * transparency + random.gauss(0.0, 0.014)))

        harm = max(
            0.0,
            min(
                1.0,
                harm
                + 0.080 * controversy
                - 0.030 * equity
                - 0.020 * responsiveness
                + random.gauss(0.0, 0.016),
            ),
        )

        legitimacy = max(
            0.0,
            min(
                1.0,
                legitimacy
                + 0.030 * transparency
                + 0.030 * participation
                + 0.030 * contestability
                + 0.030 * equity
                - 0.060 * harm
                - 0.030 * controversy
                + random.gauss(0.0, 0.014),
            ),
        )

        trust = max(
            0.0,
            min(
                1.0,
                trust
                + 0.030 * legitimacy
                + 0.020 * responsiveness
                + 0.015 * uncertainty
                - 0.070 * harm
                - 0.030 * controversy
                + random.gauss(0.0, 0.016),
            ),
        )

        review_required = (
            trust <= trust_trigger
            or legitimacy <= legitimacy_trigger
            or contestability <= contestability_trigger
            or equity <= equity_trigger
            or harm >= harm_trigger
        )

        if review_required:
            transparency = min(1.0, transparency + 0.035)
            participation = min(1.0, participation + 0.035)
            contestability = min(1.0, contestability + 0.040)
            equity = min(1.0, equity + 0.030)
            legitimacy = min(1.0, legitimacy + 0.030)
            trust = min(1.0, trust + 0.025)
            harm = max(0.0, harm - 0.030 * responsiveness)

        rows.append({
            "public_decision_system": name,
            "time": time,
            "public_trust": round(trust, 6),
            "legitimacy": round(legitimacy, 6),
            "participation": round(participation, 6),
            "evidence_transparency": round(transparency, 6),
            "contestability": round(contestability, 6),
            "equity_review": round(equity, 6),
            "uncertainty_communication": round(uncertainty, 6),
            "public_harm_signal": round(harm, 6),
            "controversy_event": controversy_event,
            "controversy_severity": round(controversy, 6),
            "review_required": review_required,
        })

    return rows


def simulate_all() -> list[dict[str, object]]:
    params = load_parameters()
    random.seed(int(params["random_seed"]))

    rows: list[dict[str, object]] = []
    for name, config in PUBLIC_DECISION_SYSTEMS.items():
        rows.extend(
            simulate_system(
                name,
                config,
                time_steps=int(params["time_steps"]),
                trust_trigger=params["trust_trigger"],
                legitimacy_trigger=params["legitimacy_trigger"],
                contestability_trigger=params["contestability_trigger"],
                equity_trigger=params["equity_trigger"],
                harm_trigger=params["harm_trigger"],
            )
        )

    return rows


def summarize(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    systems = sorted({str(row["public_decision_system"]) for row in rows})
    summary: list[dict[str, object]] = []

    for system in systems:
        system_rows = [row for row in rows if row["public_decision_system"] == system]
        trust_values = [float(row["public_trust"]) for row in system_rows]
        legitimacy_values = [float(row["legitimacy"]) for row in system_rows]
        participation_values = [float(row["participation"]) for row in system_rows]
        contestability_values = [float(row["contestability"]) for row in system_rows]
        equity_values = [float(row["equity_review"]) for row in system_rows]
        harm_values = [float(row["public_harm_signal"]) for row in system_rows]
        review_count = sum(1 for row in system_rows if bool(row["review_required"]))

        summary.append({
            "public_decision_system": system,
            "minimum_public_trust": round(min(trust_values), 6),
            "average_public_trust": round(mean(trust_values), 6),
            "minimum_legitimacy": round(min(legitimacy_values), 6),
            "minimum_participation": round(min(participation_values), 6),
            "minimum_contestability": round(min(contestability_values), 6),
            "minimum_equity_review": round(min(equity_values), 6),
            "maximum_public_harm_signal": round(max(harm_values), 6),
            "review_required_count": review_count,
            "review_flag": "review" if review_count > 0 else "acceptable",
        })

    summary.sort(key=lambda row: (float(row["average_public_trust"]), float(row["minimum_legitimacy"])), reverse=True)
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

    write_csv(TABLES / "democratic_public_reasoning_timeseries.csv", rows)
    write_csv(TABLES / "democratic_public_reasoning_summary.csv", summary_rows)

    write_json(
        RECORDS / "democratic_public_reasoning_record.json",
        {
            "article": "Decision Science and Democratic Public Reasoning",
            "decision_context": "Simulating public trust, legitimacy, participation, evidence transparency, contestability, equity review, uncertainty communication, harm signals, and review triggers.",
            "parameters": params,
            "summary_metrics": summary_rows,
            "modeling_principles": [
                "Decision science should support public reasoning, not replace democratic judgment.",
                "Public legitimacy depends on evidence, values, participation, transparency, contestability, and accountability.",
                "Trade-offs should be visible enough to debate, justify, and revise.",
                "Public trust is strengthened when uncertainty and review triggers are communicated honestly.",
                "Decision records should preserve how evidence, public input, values, dissent, and authority shaped the decision."
            ],
        },
    )

    print("Democratic public reasoning simulation complete.")
    print(TABLES / "democratic_public_reasoning_timeseries.csv")
    print(TABLES / "democratic_public_reasoning_summary.csv")
    print(RECORDS / "democratic_public_reasoning_record.json")


if __name__ == "__main__":
    main()
