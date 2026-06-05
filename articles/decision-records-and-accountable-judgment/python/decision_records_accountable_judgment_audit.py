#!/usr/bin/env python3
"""
Decision Records and Accountable Judgment Audit

Audits decision record quality, evidence traceability, assumption risk,
monitoring gaps, review triggers, and signal drift.

Uses only the Python standard library.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import csv
import json
import random
from statistics import mean

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
DATA = ARTICLE_ROOT / "data"
TABLES = ARTICLE_ROOT / "outputs" / "tables"
RECORDS = ARTICLE_ROOT / "outputs" / "decision_records"

WEIGHTS = {
    "frame_quality": 0.10,
    "alternative_quality": 0.09,
    "evidence_quality": 0.11,
    "assumption_clarity": 0.11,
    "uncertainty_quality": 0.12,
    "tradeoff_transparency": 0.10,
    "dissent_preservation": 0.09,
    "rationale_quality": 0.10,
    "monitoring_quality": 0.09,
    "review_trigger_quality": 0.09,
    "accountability_quality": 0.10,
}


@dataclass(frozen=True)
class DecisionRecord:
    record_id: str
    context: str
    frame_quality: float
    alternative_quality: float
    evidence_quality: float
    assumption_clarity: float
    uncertainty_quality: float
    tradeoff_transparency: float
    dissent_preservation: float
    rationale_quality: float
    monitoring_quality: float
    review_trigger_quality: float
    accountability_quality: float


@dataclass(frozen=True)
class Assumption:
    assumption_id: str
    record_id: str
    statement: str
    confidence: float
    criticality: float
    monitored: bool


@dataclass(frozen=True)
class Claim:
    claim_id: str
    record_id: str
    claim: str
    evidence_linked: bool
    evidence_quality: float


@dataclass(frozen=True)
class MonitoringSignal:
    signal_id: str
    record_id: str
    indicator: str
    baseline: float
    lower_bound: float
    upper_bound: float
    current_value: float
    review_owner: str


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def parse_bool(value: str) -> bool:
    return value.strip().lower() in {"true", "1", "yes", "y"}


def load_records() -> list[DecisionRecord]:
    rows = read_csv_dicts(DATA / "synthetic_decision_records.csv")
    return [
        DecisionRecord(
            row["record_id"],
            row["decision_context"],
            float(row["frame_quality"]),
            float(row["alternative_quality"]),
            float(row["evidence_quality"]),
            float(row["assumption_clarity"]),
            float(row["uncertainty_quality"]),
            float(row["tradeoff_transparency"]),
            float(row["dissent_preservation"]),
            float(row["rationale_quality"]),
            float(row["monitoring_quality"]),
            float(row["review_trigger_quality"]),
            float(row["accountability_quality"]),
        )
        for row in rows
    ]


def load_assumptions() -> list[Assumption]:
    rows = read_csv_dicts(DATA / "synthetic_assumptions.csv")
    return [
        Assumption(
            row["assumption_id"],
            row["record_id"],
            row["assumption"],
            float(row["confidence"]),
            float(row["criticality"]),
            parse_bool(row["monitored"]),
        )
        for row in rows
    ]


def load_claims() -> list[Claim]:
    rows = read_csv_dicts(DATA / "synthetic_claims.csv")
    return [
        Claim(
            row["claim_id"],
            row["record_id"],
            row["claim"],
            parse_bool(row["evidence_linked"]),
            float(row["evidence_quality"]),
        )
        for row in rows
    ]


def load_signals() -> list[MonitoringSignal]:
    rows = read_csv_dicts(DATA / "synthetic_review_triggers.csv")
    return [
        MonitoringSignal(
            row["trigger_id"],
            row["record_id"],
            row["indicator"],
            float(row["baseline"]),
            float(row["lower_bound"]),
            float(row["upper_bound"]),
            float(row["current_value"]),
            row["review_owner"],
        )
        for row in rows
    ]


def record_quality(record: DecisionRecord) -> float:
    return (
        record.frame_quality * WEIGHTS["frame_quality"]
        + record.alternative_quality * WEIGHTS["alternative_quality"]
        + record.evidence_quality * WEIGHTS["evidence_quality"]
        + record.assumption_clarity * WEIGHTS["assumption_clarity"]
        + record.uncertainty_quality * WEIGHTS["uncertainty_quality"]
        + record.tradeoff_transparency * WEIGHTS["tradeoff_transparency"]
        + record.dissent_preservation * WEIGHTS["dissent_preservation"]
        + record.rationale_quality * WEIGHTS["rationale_quality"]
        + record.monitoring_quality * WEIGHTS["monitoring_quality"]
        + record.review_trigger_quality * WEIGHTS["review_trigger_quality"]
        + record.accountability_quality * WEIGHTS["accountability_quality"]
    )


def minimum_component(record: DecisionRecord) -> float:
    return min(
        record.frame_quality,
        record.alternative_quality,
        record.evidence_quality,
        record.assumption_clarity,
        record.uncertainty_quality,
        record.tradeoff_transparency,
        record.dissent_preservation,
        record.rationale_quality,
        record.monitoring_quality,
        record.review_trigger_quality,
        record.accountability_quality,
    )


def accountable_judgment_score(record: DecisionRecord) -> float:
    return 0.70 * record_quality(record) + 0.30 * minimum_component(record)


def assumption_risk(assumption: Assumption) -> float:
    return assumption.criticality * (1.0 - assumption.confidence)


def monitoring_gap(assumption: Assumption) -> bool:
    return assumption.criticality >= 0.75 and not assumption.monitored


def signal_trigger_active(signal: MonitoringSignal) -> bool:
    return signal.current_value < signal.lower_bound or signal.current_value > signal.upper_bound


def traceability_share(claims: list[Claim]) -> float:
    if not claims:
        return 0.0
    return sum(1 for claim in claims if claim.evidence_linked) / len(claims)


def average_evidence_quality(claims: list[Claim]) -> float:
    if not claims:
        return 0.0
    return mean(claim.evidence_quality for claim in claims)


def audit_records(
    records: list[DecisionRecord],
    assumptions: list[Assumption],
    claims: list[Claim],
    signals: list[MonitoringSignal],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    for record in records:
        record_assumptions = [item for item in assumptions if item.record_id == record.record_id]
        record_claims = [item for item in claims if item.record_id == record.record_id]
        record_signals = [item for item in signals if item.record_id == record.record_id]

        avg_assumption_risk = mean([assumption_risk(item) for item in record_assumptions]) if record_assumptions else 0.0
        critical_gaps = sum(1 for item in record_assumptions if monitoring_gap(item))
        active_triggers = sum(1 for item in record_signals if signal_trigger_active(item))
        trace_share = traceability_share(record_claims)
        avg_evidence_quality = average_evidence_quality(record_claims)

        quality = accountable_judgment_score(record)
        review_priority_score = (
            0.35 * (1.0 - quality)
            + 0.20 * avg_assumption_risk
            + 0.20 * (1.0 - trace_share)
            + 0.15 * min(critical_gaps, 3) / 3
            + 0.10 * min(active_triggers, 3) / 3
        )

        if review_priority_score >= 0.45:
            priority = "high"
        elif review_priority_score >= 0.25:
            priority = "medium"
        else:
            priority = "low"

        rows.append({
            "record_id": record.record_id,
            "context": record.context,
            "record_quality": round(record_quality(record), 4),
            "minimum_component": round(minimum_component(record), 4),
            "accountable_judgment_score": round(quality, 4),
            "traceability_share": round(trace_share, 4),
            "average_evidence_quality": round(avg_evidence_quality, 4),
            "average_assumption_risk": round(avg_assumption_risk, 4),
            "critical_monitoring_gaps": critical_gaps,
            "active_review_triggers": active_triggers,
            "review_priority_score": round(review_priority_score, 4),
            "review_priority": priority,
        })

    return sorted(rows, key=lambda row: float(row["review_priority_score"]), reverse=True)


def simulate_signal_drift(signals: list[MonitoringSignal], periods: int = 12, seed: int = 42) -> list[dict[str, object]]:
    rng = random.Random(seed)
    rows: list[dict[str, object]] = []

    for signal in signals:
        value = signal.current_value
        for period in range(1, periods + 1):
            value = value + rng.gauss(0.0, 0.08)
            active = value < signal.lower_bound or value > signal.upper_bound
            rows.append({
                "period": period,
                "signal_id": signal.signal_id,
                "record_id": signal.record_id,
                "indicator": signal.indicator,
                "value": round(value, 4),
                "lower_bound": signal.lower_bound,
                "upper_bound": signal.upper_bound,
                "review_owner": signal.review_owner,
                "review_trigger_active": active,
            })

    return rows


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
    records = load_records()
    assumptions = load_assumptions()
    claims = load_claims()
    signals = load_signals()

    audit_rows = audit_records(records, assumptions, claims, signals)
    drift_rows = simulate_signal_drift(signals, periods=12, seed=42)

    assumption_rows = [
        {
            "assumption_id": item.assumption_id,
            "record_id": item.record_id,
            "statement": item.statement,
            "confidence": item.confidence,
            "criticality": item.criticality,
            "monitored": item.monitored,
            "assumption_risk": round(assumption_risk(item), 4),
            "monitoring_gap": monitoring_gap(item),
        }
        for item in assumptions
    ]

    claim_rows = [
        {
            "claim_id": item.claim_id,
            "record_id": item.record_id,
            "claim": item.claim,
            "evidence_linked": item.evidence_linked,
            "evidence_quality": item.evidence_quality,
        }
        for item in claims
    ]

    write_csv(TABLES / "decision_record_audit_summary.csv", audit_rows)
    write_csv(TABLES / "decision_record_assumption_audit.csv", assumption_rows)
    write_csv(TABLES / "decision_record_claim_traceability.csv", claim_rows)
    write_csv(TABLES / "decision_record_signal_drift.csv", drift_rows)

    write_json(
        RECORDS / "decision_record_template.json",
        {
            "article": "Decision Records and Accountable Judgment",
            "purpose": "Preserve the reasoning architecture behind consequential decisions.",
            "record_fields": {
                "decision_frame": "",
                "decision_owner": "",
                "alternatives_considered": [],
                "evidence": [],
                "assumptions": [],
                "uncertainties": [],
                "criteria": [],
                "tradeoffs": [],
                "dissent": [],
                "selected_action": "",
                "rationale": "",
                "implementation_owner": "",
                "monitoring_indicators": [],
                "review_triggers": [],
            },
            "audit_summary": audit_rows,
        },
    )

    print("Decision record audit complete.")
    print(TABLES / "decision_record_audit_summary.csv")
    print(TABLES / "decision_record_signal_drift.csv")
    print(RECORDS / "decision_record_template.json")


if __name__ == "__main__":
    main()
