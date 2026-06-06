#!/usr/bin/env python3
"""
Group Decision-Making and Social Influence Simulation

Simulates independent judgment, social influence, authority weighting,
consensus pressure, hidden-profile risk, dissent, collective error,
review queues, and decision-record export.

Uses only the Python standard library.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import csv
import json
import math
import random
from statistics import mean

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
DATA = ARTICLE_ROOT / "data"
TABLES = ARTICLE_ROOT / "outputs" / "tables"
RECORDS = ARTICLE_ROOT / "outputs" / "decision_records"


@dataclass(frozen=True)
class GroupCase:
    group_id: int
    domain: str
    true_value: float
    authority_concentration: float
    consensus_pressure: float
    shared_information: int
    unique_information: int
    members_per_group: int = 7


def clamp(value: float, low: float = 0.01, high: float = 0.99) -> float:
    return max(low, min(high, value))


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def load_seed_groups() -> list[GroupCase]:
    rows = read_csv_dicts(DATA / "synthetic_group_cases.csv")
    return [
        GroupCase(
            group_id=int(row["group_id"]),
            domain=row["domain"],
            true_value=float(row["true_value"]),
            authority_concentration=float(row["authority_concentration"]),
            consensus_pressure=float(row["consensus_pressure"]),
            shared_information=int(row["shared_information"]),
            unique_information=int(row["unique_information"]),
            members_per_group=int(row["members_per_group"]),
        )
        for row in rows
    ]


def generate_group_cases(n_groups: int = 240, seed: int = 42) -> list[GroupCase]:
    rng = random.Random(seed)
    domains = [
        "Public Policy",
        "Healthcare",
        "Financial Risk",
        "Infrastructure",
        "AI Governance",
        "Organizational Strategy",
    ]

    cases = load_seed_groups()

    for group_id in range(len(cases) + 1, n_groups + 1):
        cases.append(
            GroupCase(
                group_id=group_id,
                domain=rng.choice(domains),
                true_value=rng.uniform(0.20, 0.85),
                authority_concentration=rng.uniform(0.10, 0.60),
                consensus_pressure=rng.uniform(0.05, 0.75),
                shared_information=rng.randint(4, 12),
                unique_information=rng.randint(1, 10),
                members_per_group=7,
            )
        )

    return cases


def information_entropy(shared_information: int, unique_information: int) -> float:
    total = shared_information + unique_information
    if total == 0:
        return 0.0
    values = [shared_information / total, unique_information / total]
    return -sum(p * math.log(p) for p in values if p > 0)


def hidden_profile_risk(shared_information: int, unique_information: int) -> float:
    total = shared_information + unique_information
    if total == 0:
        return 0.0
    return unique_information / total


def simulate_members(group: GroupCase, rng: random.Random) -> list[dict[str, object]]:
    expertise = [rng.uniform(0.30, 0.95) for _ in range(group.members_per_group)]
    status = [rng.uniform(0.10, 0.95) for _ in range(group.members_per_group)]

    status[0] = max(status[0], 0.90)
    expertise[0] = rng.uniform(0.45, 0.90)

    independent_estimates: list[float] = []
    for member_index in range(group.members_per_group):
        noise = rng.gauss(0.0, 0.22 * (1.0 - expertise[member_index]))
        independent_estimates.append(clamp(group.true_value + noise))

    initial_majority = mean(independent_estimates)

    influenced_estimates = [
        clamp((1.0 - group.consensus_pressure) * estimate + group.consensus_pressure * initial_majority)
        for estimate in independent_estimates
    ]

    raw_weights = [
        (1.0 - group.authority_concentration) * expertise[i]
        + group.authority_concentration * status[i]
        for i in range(group.members_per_group)
    ]
    weight_total = sum(raw_weights)
    influence_weights = [weight / weight_total for weight in raw_weights]

    rows: list[dict[str, object]] = []
    for member_id in range(1, group.members_per_group + 1):
        i = member_id - 1
        rows.append({
            "group_id": group.group_id,
            "domain": group.domain,
            "member_id": member_id,
            "expertise": round(expertise[i], 6),
            "status": round(status[i], 6),
            "independent_estimate": round(independent_estimates[i], 6),
            "influenced_estimate": round(influenced_estimates[i], 6),
            "influence_weight": round(influence_weights[i], 6),
            "true_value": round(group.true_value, 6),
        })

    return rows


def summarize_group(group: GroupCase, member_rows: list[dict[str, object]]) -> dict[str, object]:
    independent_estimates = [float(row["independent_estimate"]) for row in member_rows]
    influenced_estimates = [float(row["influenced_estimate"]) for row in member_rows]
    weights = [float(row["influence_weight"]) for row in member_rows]

    independent_group_estimate = mean(independent_estimates)
    influenced_group_estimate = sum(estimate * weight for estimate, weight in zip(influenced_estimates, weights))

    independent_error = abs(independent_group_estimate - group.true_value)
    collective_error = abs(influenced_group_estimate - group.true_value)
    social_influence_error_change = collective_error - independent_error

    dissent_ratio = sum(
        1 for estimate in independent_estimates
        if abs(estimate - independent_group_estimate) > 0.12
    ) / len(independent_estimates)

    influence_concentration = max(weights)
    hp_risk = hidden_profile_risk(group.shared_information, group.unique_information)
    entropy = information_entropy(group.shared_information, group.unique_information)

    review = (
        collective_error > 0.15
        or social_influence_error_change > 0.05
        or influence_concentration > 0.35
        or hp_risk > 0.45
        or group.consensus_pressure > 0.60
    )

    return {
        "group_id": group.group_id,
        "domain": group.domain,
        "true_value": round(group.true_value, 6),
        "independent_group_estimate": round(independent_group_estimate, 6),
        "influenced_group_estimate": round(influenced_group_estimate, 6),
        "independent_error": round(independent_error, 6),
        "collective_error": round(collective_error, 6),
        "social_influence_error_change": round(social_influence_error_change, 6),
        "dissent_ratio": round(dissent_ratio, 6),
        "influence_concentration": round(influence_concentration, 6),
        "consensus_pressure": round(group.consensus_pressure, 6),
        "authority_concentration": round(group.authority_concentration, 6),
        "shared_information": group.shared_information,
        "unique_information": group.unique_information,
        "hidden_profile_risk": round(hp_risk, 6),
        "evidence_diversity": round(entropy, 6),
        "review_flag": "review" if review else "acceptable",
    }


def group_summary_by_field(rows: list[dict[str, object]], field: str) -> list[dict[str, object]]:
    output: list[dict[str, object]] = []

    for group_value in sorted({str(row[field]) for row in rows}):
        subset = [row for row in rows if str(row[field]) == group_value]
        output.append({
            field: group_value,
            "n_groups": len(subset),
            "average_collective_error": round(mean(float(row["collective_error"]) for row in subset), 6),
            "average_independent_error": round(mean(float(row["independent_error"]) for row in subset), 6),
            "average_social_influence_error_change": round(mean(float(row["social_influence_error_change"]) for row in subset), 6),
            "average_dissent_ratio": round(mean(float(row["dissent_ratio"]) for row in subset), 6),
            "average_influence_concentration": round(mean(float(row["influence_concentration"]) for row in subset), 6),
            "average_hidden_profile_risk": round(mean(float(row["hidden_profile_risk"]) for row in subset), 6),
            "average_consensus_pressure": round(mean(float(row["consensus_pressure"]) for row in subset), 6),
            "review_rate": round(sum(1 for row in subset if row["review_flag"] == "review") / len(subset), 6),
        })

    return output


def overall_metrics(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {"metric": "mean_collective_error", "value": round(mean(float(row["collective_error"]) for row in rows), 6)},
        {"metric": "mean_independent_error", "value": round(mean(float(row["independent_error"]) for row in rows), 6)},
        {"metric": "mean_social_influence_error_change", "value": round(mean(float(row["social_influence_error_change"]) for row in rows), 6)},
        {"metric": "mean_dissent_ratio", "value": round(mean(float(row["dissent_ratio"]) for row in rows), 6)},
        {"metric": "mean_influence_concentration", "value": round(mean(float(row["influence_concentration"]) for row in rows), 6)},
        {"metric": "mean_hidden_profile_risk", "value": round(mean(float(row["hidden_profile_risk"]) for row in rows), 6)},
        {"metric": "mean_consensus_pressure", "value": round(mean(float(row["consensus_pressure"]) for row in rows), 6)},
        {"metric": "review_rate", "value": round(sum(1 for row in rows if row["review_flag"] == "review") / len(rows), 6)},
    ]


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
    rng = random.Random(123)
    groups = generate_group_cases(n_groups=240, seed=42)

    all_member_rows: list[dict[str, object]] = []
    group_rows: list[dict[str, object]] = []

    for group in groups:
        member_rows = simulate_members(group, rng)
        all_member_rows.extend(member_rows)
        group_rows.append(summarize_group(group, member_rows))

    domain_rows = group_summary_by_field(group_rows, "domain")
    review_rows = [row for row in group_rows if row["review_flag"] == "review"]
    metrics = overall_metrics(group_rows)

    write_csv(TABLES / "group_member_estimates.csv", all_member_rows)
    write_csv(TABLES / "group_decision_summary.csv", group_rows)
    write_csv(TABLES / "domain_group_decision_summary.csv", domain_rows)
    write_csv(TABLES / "group_decision_review_queue.csv", review_rows)
    write_csv(TABLES / "overall_group_decision_metrics.csv", metrics)

    write_json(
        RECORDS / "group_decision_record.json",
        {
            "article": "Group Decision-Making and Social Influence",
            "decision_context": "Evaluating group judgment, social influence, hidden-profile risk, dissent, influence concentration, and collective error.",
            "modeling_principles": [
                "Group judgment should preserve independent estimates before discussion.",
                "Social influence should be measured through influence weights, consensus pressure, and authority concentration.",
                "Unique information should be elicited so hidden profiles do not disappear.",
                "Dissent should be recorded rather than smoothed into consensus.",
                "Decision records should preserve evidence, disagreement, confidence, decision rules, and review triggers.",
            ],
            "overall_metrics": metrics,
            "domain_summary": domain_rows,
            "review_queue_size": len(review_rows),
        },
    )

    print("Group decision-making and social influence workflow complete.")
    print(TABLES / "group_member_estimates.csv")
    print(TABLES / "group_decision_summary.csv")
    print(TABLES / "domain_group_decision_summary.csv")
    print(TABLES / "group_decision_review_queue.csv")
    print(RECORDS / "group_decision_record.json")


if __name__ == "__main__":
    main()
