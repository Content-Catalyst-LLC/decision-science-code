#!/usr/bin/env python3
"""
Decision Quality Architecture Simulation

Simulates decision quality as a process standard distinct from outcome quality.

Uses only the Python standard library.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import csv
import json
import random
from statistics import mean, pstdev

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
DATA = ARTICLE_ROOT / "data"
TABLES = ARTICLE_ROOT / "outputs" / "tables"
RECORDS = ARTICLE_ROOT / "outputs" / "decision_records"

WEIGHTS = {
    "framing_quality": 0.11,
    "alternative_quality": 0.10,
    "evidence_quality": 0.12,
    "uncertainty_quality": 0.13,
    "tradeoff_clarity": 0.11,
    "behavioral_safeguards": 0.10,
    "systems_awareness": 0.11,
    "accountability": 0.11,
    "learning_design": 0.11,
}


@dataclass(frozen=True)
class Alternative:
    name: str
    framing_quality: float
    alternative_quality: float
    evidence_quality: float
    uncertainty_quality: float
    tradeoff_clarity: float
    behavioral_safeguards: float
    systems_awareness: float
    accountability: float
    learning_design: float
    expected_value: float
    downside_exposure: float


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def load_alternatives() -> list[Alternative]:
    rows = read_csv_dicts(DATA / "synthetic_decision_profiles.csv")
    return [
        Alternative(
            row["alternative"],
            float(row["framing_quality"]),
            float(row["alternative_quality"]),
            float(row["evidence_quality"]),
            float(row["uncertainty_quality"]),
            float(row["tradeoff_clarity"]),
            float(row["behavioral_safeguards"]),
            float(row["systems_awareness"]),
            float(row["accountability"]),
            float(row["learning_design"]),
            float(row["expected_value"]),
            float(row["downside_exposure"]),
        )
        for row in rows
    ]


def decision_quality_score(alternative: Alternative) -> float:
    return (
        alternative.framing_quality * WEIGHTS["framing_quality"]
        + alternative.alternative_quality * WEIGHTS["alternative_quality"]
        + alternative.evidence_quality * WEIGHTS["evidence_quality"]
        + alternative.uncertainty_quality * WEIGHTS["uncertainty_quality"]
        + alternative.tradeoff_clarity * WEIGHTS["tradeoff_clarity"]
        + alternative.behavioral_safeguards * WEIGHTS["behavioral_safeguards"]
        + alternative.systems_awareness * WEIGHTS["systems_awareness"]
        + alternative.accountability * WEIGHTS["accountability"]
        + alternative.learning_design * WEIGHTS["learning_design"]
    )


def minimum_component_score(alternative: Alternative) -> float:
    return min(
        alternative.framing_quality,
        alternative.alternative_quality,
        alternative.evidence_quality,
        alternative.uncertainty_quality,
        alternative.tradeoff_clarity,
        alternative.behavioral_safeguards,
        alternative.systems_awareness,
        alternative.accountability,
        alternative.learning_design,
    )


def architecture_score(alternative: Alternative) -> float:
    quality = decision_quality_score(alternative)
    minimum = minimum_component_score(alternative)
    return 0.70 * quality + 0.30 * minimum


def simulate_outcome(alternative: Alternative, rng: random.Random) -> float:
    external_shock = rng.gauss(0.0, 22.0)
    implementation_noise = rng.gauss(0.0, 8.0)
    adverse_exposure = max(0.0, rng.gauss(0.45, 0.30))

    downside_penalty = 45.0 * alternative.downside_exposure * adverse_exposure
    learning_credit = 18.0 * alternative.learning_design
    accountability_credit = 14.0 * alternative.accountability
    safeguards_credit = 10.0 * alternative.behavioral_safeguards

    return (
        alternative.expected_value
        - downside_penalty
        + learning_credit
        + accountability_credit
        + safeguards_credit
        + external_shock
        + implementation_noise
    )


def classify_case(alternative: Alternative, outcome: float) -> str:
    process_good = decision_quality_score(alternative) >= 0.80
    outcome_good = outcome >= 75.0

    if process_good and outcome_good:
        return "good process and good outcome"
    if process_good and not outcome_good:
        return "good process exposed to unfavorable uncertainty"
    if not process_good and outcome_good:
        return "weak process with favorable outcome; possible luck"
    return "weak process and weak outcome"


def simulate(alternatives: list[Alternative], trials: int = 1000, seed: int = 42) -> list[dict[str, object]]:
    rng = random.Random(seed)
    rows: list[dict[str, object]] = []

    for alternative in alternatives:
        for trial in range(1, trials + 1):
            outcome = simulate_outcome(alternative, rng)
            quality = decision_quality_score(alternative)
            architecture = architecture_score(alternative)
            review_trigger = (
                outcome < 60.0
                or quality < 0.65
                or alternative.uncertainty_quality < 0.55
                or alternative.accountability < 0.55
                or alternative.downside_exposure > 0.65
            )

            rows.append({
                "trial": trial,
                "alternative": alternative.name,
                "decision_quality_score": round(quality, 4),
                "architecture_score": round(architecture, 4),
                "minimum_component_score": round(minimum_component_score(alternative), 4),
                "outcome": round(outcome, 4),
                "favorable_outcome": outcome >= 75.0,
                "review_trigger": review_trigger,
                "case_classification": classify_case(alternative, outcome),
            })

    return rows


def summarize(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    alternatives = sorted({str(row["alternative"]) for row in rows})
    output: list[dict[str, object]] = []

    for alternative in alternatives:
        alt_rows = [row for row in rows if row["alternative"] == alternative]
        outcomes = [float(row["outcome"]) for row in alt_rows]
        favorable = [bool(row["favorable_outcome"]) for row in alt_rows]
        review = [bool(row["review_trigger"]) for row in alt_rows]

        quality = float(alt_rows[0]["decision_quality_score"])
        architecture = float(alt_rows[0]["architecture_score"])
        minimum_component = float(alt_rows[0]["minimum_component_score"])

        output.append({
            "alternative": alternative,
            "decision_quality_score": round(quality, 4),
            "architecture_score": round(architecture, 4),
            "minimum_component_score": round(minimum_component, 4),
            "mean_outcome": round(mean(outcomes), 4),
            "minimum_outcome": round(min(outcomes), 4),
            "maximum_outcome": round(max(outcomes), 4),
            "outcome_sd": round(pstdev(outcomes), 4),
            "favorable_outcome_rate": round(sum(1 for item in favorable if item) / len(favorable), 4),
            "review_trigger_rate": round(sum(1 for item in review if item) / len(review), 4),
        })

    for row in output:
        if row["decision_quality_score"] < 0.60 and row["favorable_outcome_rate"] > 0.50:
            row["interpretation"] = "possible luck masking weak process"
        elif row["decision_quality_score"] >= 0.80 and row["favorable_outcome_rate"] < 0.50:
            row["interpretation"] = "sound process exposed to unfavorable uncertainty"
        else:
            row["interpretation"] = "process and outcome broadly aligned"

    return sorted(output, key=lambda row: float(row["architecture_score"]), reverse=True)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"No rows to write: {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_decision_record(path: Path, summary_rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    record = {
        "article": "Decision Quality and the Architecture of Judgment",
        "decision_context": "Simulation separating decision-process quality from realized outcome quality.",
        "highest_architecture_score": summary_rows[0]["alternative"],
        "interpretation": "Decision quality is evaluated as a process standard rather than a guarantee of favorable outcome.",
        "modeling_principles": [
            "Separate decision quality from outcome quality.",
            "Evaluate framing, alternatives, evidence, uncertainty, trade-offs, safeguards, systems awareness, accountability, and learning.",
            "Treat favorable outcomes from weak processes as possible luck.",
            "Treat unfavorable outcomes from strong processes as opportunities for assumption review, not automatic blame.",
            "Use decision records to reduce hindsight bias and support institutional learning.",
        ],
        "summary": summary_rows,
    }

    path.write_text(json.dumps(record, indent=2), encoding="utf-8")


def main() -> None:
    alternatives = load_alternatives()
    rows = simulate(alternatives, trials=1000, seed=42)
    summary_rows = summarize(rows)

    write_csv(TABLES / "decision_quality_simulation_trials.csv", rows)
    write_csv(TABLES / "decision_quality_summary.csv", summary_rows)
    write_decision_record(RECORDS / "decision_quality_architecture_record.json", summary_rows)

    print("Decision quality architecture simulation complete.")
    print(TABLES / "decision_quality_summary.csv")
    print(RECORDS / "decision_quality_architecture_record.json")


if __name__ == "__main__":
    main()
