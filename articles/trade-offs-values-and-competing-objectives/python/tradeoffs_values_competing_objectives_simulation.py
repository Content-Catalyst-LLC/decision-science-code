#!/usr/bin/env python3
"""
Trade-Offs, Values, and Competing Objectives workflow.

Simulates weighted competing objectives, priority sensitivity,
dominated-option analysis, scenario regret, rank stability,
review flags, and decision-record export.

Uses only the Python standard library.
"""

from __future__ import annotations

from pathlib import Path
import csv
import json
import random
from statistics import mean, stdev

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
DATA = ARTICLE_ROOT / "data"
TABLES = ARTICLE_ROOT / "outputs" / "tables"
RECORDS = ARTICLE_ROOT / "outputs" / "decision_records"

OBJECTIVES = [
    "cost_efficiency",
    "equity",
    "resilience",
    "long_term_value",
    "legitimacy",
    "reversibility",
]


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def load_alternatives() -> list[dict[str, object]]:
    rows = read_csv_dicts(DATA / "synthetic_alternatives.csv")
    output: list[dict[str, object]] = []
    for row in rows:
        item: dict[str, object] = {"alternative": row["alternative"]}
        for objective in OBJECTIVES:
            item[objective] = float(row[objective])
        output.append(item)
    return output


def load_weights(path: Path, key_field: str = "objective", value_field: str = "weight") -> dict[str, float]:
    rows = read_csv_dicts(path)
    weights = {row[key_field]: float(row[value_field]) for row in rows}
    ensure_weights(weights)
    return weights


def load_scenario_weights() -> dict[str, dict[str, float]]:
    rows = read_csv_dicts(DATA / "synthetic_scenario_weights.csv")
    scenarios = sorted({row["scenario"] for row in rows})
    output: dict[str, dict[str, float]] = {}
    for scenario in scenarios:
        weights = {
            row["objective"]: float(row["weight"])
            for row in rows
            if row["scenario"] == scenario
        }
        ensure_weights(weights)
        output[scenario] = weights
    return output


def load_stakeholder_profiles() -> dict[str, dict[str, float]]:
    rows = read_csv_dicts(DATA / "synthetic_stakeholder_profiles.csv")
    profiles = sorted({row["profile"] for row in rows})
    output: dict[str, dict[str, float]] = {}
    for profile in profiles:
        weights = {
            row["objective"]: float(row["weight"])
            for row in rows
            if row["profile"] == profile
        }
        ensure_weights(weights)
        output[profile] = weights
    return output


def ensure_weights(weights: dict[str, float]) -> None:
    total = sum(weights.values())
    if abs(total - 1.0) > 1e-9:
        raise ValueError(f"Weights must sum to 1. Got {total}.")
    for objective in OBJECTIVES:
        if objective not in weights:
            raise ValueError(f"Missing objective weight: {objective}")


def weighted_score(row: dict[str, object], weights: dict[str, float]) -> float:
    return sum(float(row[objective]) * weights[objective] for objective in OBJECTIVES)


def rank_rows(rows: list[dict[str, object]], score_field: str = "composite_score") -> list[dict[str, object]]:
    sorted_rows = sorted(rows, key=lambda row: float(row[score_field]), reverse=True)
    output: list[dict[str, object]] = []
    for rank, row in enumerate(sorted_rows, start=1):
        item = dict(row)
        item["rank"] = rank
        output.append(item)
    return output


def random_weight_vector(rng: random.Random, base_weights: dict[str, float], concentration: float = 70.0) -> dict[str, float]:
    draws = {
        objective: rng.gammavariate(max(base_weights[objective] * concentration, 0.001), 1.0)
        for objective in OBJECTIVES
    }
    total = sum(draws.values())
    return {objective: value / total for objective, value in draws.items()}


def dominated_options(alternatives: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for alternative_a in alternatives:
        dominator_count = 0
        for alternative_b in alternatives:
            if alternative_a["alternative"] == alternative_b["alternative"]:
                continue
            b_at_least_as_good = all(float(alternative_b[obj]) >= float(alternative_a[obj]) for obj in OBJECTIVES)
            b_strictly_better_somewhere = any(float(alternative_b[obj]) > float(alternative_a[obj]) for obj in OBJECTIVES)
            if b_at_least_as_good and b_strictly_better_somewhere:
                dominator_count += 1
        rows.append({
            "alternative": alternative_a["alternative"],
            "dominated_by_any": dominator_count > 0,
            "dominator_count": dominator_count,
        })
    return rows


def objective_contributions(alternatives: list[dict[str, object]], weights: dict[str, float]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for alternative in alternatives:
        row: dict[str, object] = {"alternative": alternative["alternative"]}
        total = 0.0
        for objective in OBJECTIVES:
            value = float(alternative[objective]) * weights[objective]
            row[objective] = round(value, 6)
            total += value
        row["total_score"] = round(total, 6)
        rows.append(row)
    return rows


def scenario_regret(alternatives: list[dict[str, object]], scenario_weights: dict[str, dict[str, float]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for scenario, weights in scenario_weights.items():
        scored = [
            {
                "scenario": scenario,
                "alternative": alternative["alternative"],
                "scenario_score": weighted_score(alternative, weights),
            }
            for alternative in alternatives
        ]
        ranked = rank_rows(scored, score_field="scenario_score")
        best_score = max(float(row["scenario_score"]) for row in ranked)
        for row in ranked:
            rows.append({
                "scenario": scenario,
                "alternative": row["alternative"],
                "scenario_score": round(float(row["scenario_score"]), 6),
                "regret": round(best_score - float(row["scenario_score"]), 6),
                "rank": row["rank"],
            })
    return rows


def stakeholder_profile_results(alternatives: list[dict[str, object]], profiles: dict[str, dict[str, float]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for profile, weights in profiles.items():
        scored = [
            {
                "profile": profile,
                "alternative": alternative["alternative"],
                "profile_score": round(weighted_score(alternative, weights), 6),
            }
            for alternative in alternatives
        ]
        rows.extend(rank_rows(scored, score_field="profile_score"))
    return rows


def summarize_regret(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    output: list[dict[str, object]] = []
    for alternative in sorted({str(row["alternative"]) for row in rows}):
        subset = [row for row in rows if row["alternative"] == alternative]
        regrets = [float(row["regret"]) for row in subset]
        ranks = [int(row["rank"]) for row in subset]
        output.append({
            "alternative": alternative,
            "average_regret": round(mean(regrets), 6),
            "max_regret": round(max(regrets), 6),
            "average_rank": round(mean(ranks), 6),
            "worst_rank": max(ranks),
        })
    return sorted(output, key=lambda row: (float(row["max_regret"]), float(row["average_regret"])))


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
    alternatives = load_alternatives()
    base_weights = load_weights(DATA / "synthetic_weights.csv")
    scenario_weights = load_scenario_weights()
    stakeholder_profiles = load_stakeholder_profiles()
    rng = random.Random(42)

    scored = [
        {
            "alternative": alternative["alternative"],
            "composite_score": round(weighted_score(alternative, base_weights), 6),
        }
        for alternative in alternatives
    ]
    base_results = rank_rows(scored)

    n_simulations = 3000
    simulation_rows: list[dict[str, object]] = []

    for simulation_id in range(1, n_simulations + 1):
        weights = random_weight_vector(rng, base_weights)
        sim_scored = [
            {
                "alternative": alternative["alternative"],
                "score": weighted_score(alternative, weights),
            }
            for alternative in alternatives
        ]
        sim_ranked = rank_rows(sim_scored, score_field="score")
        for row in sim_ranked:
            simulation_rows.append({
                "simulation_id": simulation_id,
                "alternative": row["alternative"],
                "score": round(float(row["score"]), 6),
                "rank": row["rank"],
            })

    rank_summary: list[dict[str, object]] = []
    for alternative in sorted({str(row["alternative"]) for row in simulation_rows}):
        subset = [row for row in simulation_rows if row["alternative"] == alternative]
        ranks = [int(row["rank"]) for row in subset]
        scores = [float(row["score"]) for row in subset]
        rank_summary.append({
            "alternative": alternative,
            "average_score": round(mean(scores), 6),
            "min_score": round(min(scores), 6),
            "max_score": round(max(scores), 6),
            "average_rank": round(mean(ranks), 6),
            "best_rank_rate": round(sum(1 for rank in ranks if rank == 1) / len(ranks), 6),
            "top_two_rate": round(sum(1 for rank in ranks if rank <= 2) / len(ranks), 6),
            "rank_volatility": round(stdev(ranks), 6),
        })
    rank_summary = sorted(rank_summary, key=lambda row: (-float(row["best_rank_rate"]), float(row["average_rank"])))

    dominance_rows = dominated_options(alternatives)
    contribution_rows = objective_contributions(alternatives, base_weights)
    regret_rows = scenario_regret(alternatives, scenario_weights)
    regret_summary = summarize_regret(regret_rows)
    stakeholder_rows = stakeholder_profile_results(alternatives, stakeholder_profiles)

    rank_summary_by_name = {row["alternative"]: row for row in rank_summary}
    regret_summary_by_name = {row["alternative"]: row for row in regret_summary}
    dominance_by_name = {row["alternative"]: row for row in dominance_rows}

    review_rows: list[dict[str, object]] = []
    for row in base_results:
        alternative = str(row["alternative"])
        stability = rank_summary_by_name[alternative]
        regret = regret_summary_by_name[alternative]
        dominance = dominance_by_name[alternative]
        review = (
            bool(dominance["dominated_by_any"])
            or float(stability["best_rank_rate"]) < 0.25
            or float(stability["rank_volatility"]) > 1.25
            or float(regret["max_regret"]) > 0.20
        )
        review_rows.append({
            "alternative": alternative,
            "base_rank": row["rank"],
            "base_score": row["composite_score"],
            "best_rank_rate": stability["best_rank_rate"],
            "top_two_rate": stability["top_two_rate"],
            "rank_volatility": stability["rank_volatility"],
            "average_regret": regret["average_regret"],
            "max_regret": regret["max_regret"],
            "dominated_by_any": dominance["dominated_by_any"],
            "review_flag": "review" if review else "acceptable",
        })

    write_csv(TABLES / "tradeoff_objective_profiles.csv", alternatives)
    write_csv(TABLES / "tradeoff_base_weights.csv", [{"objective": key, "weight": value} for key, value in base_weights.items()])
    write_csv(TABLES / "tradeoff_base_results.csv", base_results)
    write_csv(TABLES / "tradeoff_priority_sensitivity_simulations.csv", simulation_rows)
    write_csv(TABLES / "tradeoff_rank_stability_summary.csv", rank_summary)
    write_csv(TABLES / "tradeoff_dominated_options.csv", dominance_rows)
    write_csv(TABLES / "tradeoff_objective_contributions.csv", contribution_rows)
    write_csv(TABLES / "tradeoff_scenario_regret_table.csv", regret_rows)
    write_csv(TABLES / "tradeoff_regret_summary.csv", regret_summary)
    write_csv(TABLES / "tradeoff_stakeholder_profile_results.csv", stakeholder_rows)
    write_csv(TABLES / "tradeoff_review_flags.csv", review_rows)

    write_json(
        RECORDS / "tradeoff_decision_record.json",
        {
            "article": "Trade-Offs, Values, and Competing Objectives",
            "decision_context": "Comparing alternatives across cost efficiency, equity, resilience, long-term value, legitimacy, and reversibility.",
            "objectives": OBJECTIVES,
            "base_weights": base_weights,
            "scenario_weights": scenario_weights,
            "base_results": base_results,
            "rank_stability": rank_summary,
            "regret_summary": regret_summary,
            "stakeholder_profile_results": stakeholder_rows,
            "review_flags": review_rows,
            "modeling_principles": [
                "Trade-offs should be made explicit rather than hidden behind one metric.",
                "Weights encode value judgments and should be documented.",
                "Dominated options should be identified before accepting sacrifice.",
                "Rank stability and regret are useful for testing trade-offs under changing priorities.",
                "Decision records should preserve what was sacrificed, protected, and assumed.",
            ],
        },
    )

    print("Trade-off analysis workflow complete.")
    print(TABLES / "tradeoff_base_results.csv")
    print(TABLES / "tradeoff_rank_stability_summary.csv")
    print(TABLES / "tradeoff_regret_summary.csv")
    print(TABLES / "tradeoff_review_flags.csv")
    print(RECORDS / "tradeoff_decision_record.json")


if __name__ == "__main__":
    main()
