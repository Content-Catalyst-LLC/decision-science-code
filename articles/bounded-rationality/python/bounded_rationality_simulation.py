#!/usr/bin/env python3
"""
Bounded Rationality Simulation

Simulates bounded search, satisficing versus optimization,
search costs, opportunity loss, adaptive aspiration, domain
diagnostics, review queues, and decision-record export.

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
TABLES = ARTICLE_ROOT / "outputs" / "tables"
RECORDS = ARTICLE_ROOT / "outputs" / "decision_records"


@dataclass(frozen=True)
class Option:
    cycle: int
    domain: str
    option_id: int
    aspiration: float
    search_cost_per_option: float
    raw_utility: float
    implementation_risk: float
    uncertainty_penalty: float

    @property
    def adjusted_utility(self) -> float:
        return max(0.0, self.raw_utility - self.implementation_risk - self.uncertainty_penalty)

    @property
    def cumulative_search_cost(self) -> float:
        return self.option_id * self.search_cost_per_option

    @property
    def net_value(self) -> float:
        return self.adjusted_utility - self.cumulative_search_cost

    @property
    def satisfies_aspiration(self) -> bool:
        return self.adjusted_utility >= self.aspiration


def clamp(value: float, low: float = 0.05, high: float = 0.98) -> float:
    return max(low, min(high, value))


def generate_option_search_cases(
    n_cycles: int = 500,
    n_options: int = 12,
    seed: int = 42,
) -> list[Option]:
    rng = random.Random(seed)
    domains = [
        "Public Policy",
        "Healthcare",
        "Financial Risk",
        "Infrastructure",
        "AI Governance",
        "Organizational Strategy",
    ]
    options: list[Option] = []

    for cycle in range(1, n_cycles + 1):
        domain = rng.choice(domains)
        aspiration = rng.uniform(0.55, 0.82)
        search_cost = rng.uniform(0.005, 0.035)
        uncertainty_penalty = rng.uniform(0.00, 0.08)

        for option_id in range(1, n_options + 1):
            raw_utility = clamp(rng.gauss(0.68, 0.14))
            implementation_risk = rng.uniform(0.00, 0.20)
            options.append(
                Option(
                    cycle=cycle,
                    domain=domain,
                    option_id=option_id,
                    aspiration=aspiration,
                    search_cost_per_option=search_cost,
                    raw_utility=raw_utility,
                    implementation_risk=implementation_risk,
                    uncertainty_penalty=uncertainty_penalty,
                )
            )

    return options


def option_rows(options: list[Option]) -> list[dict[str, object]]:
    return [
        {
            "cycle": option.cycle,
            "domain": option.domain,
            "option_id": option.option_id,
            "aspiration": round(option.aspiration, 6),
            "search_cost_per_option": round(option.search_cost_per_option, 6),
            "raw_utility": round(option.raw_utility, 6),
            "implementation_risk": round(option.implementation_risk, 6),
            "uncertainty_penalty": round(option.uncertainty_penalty, 6),
            "adjusted_utility": round(option.adjusted_utility, 6),
            "cumulative_search_cost": round(option.cumulative_search_cost, 6),
            "net_value": round(option.net_value, 6),
            "satisfies_aspiration": option.satisfies_aspiration,
        }
        for option in options
    ]


def cycle_summary(options: list[Option]) -> list[dict[str, object]]:
    output: list[dict[str, object]] = []

    for cycle in sorted({option.cycle for option in options}):
        subset = [option for option in options if option.cycle == cycle]
        optimizing = max(subset, key=lambda option: option.adjusted_utility)

        satisfying = [option for option in subset if option.satisfies_aspiration]
        if satisfying:
            satisficing = min(satisfying, key=lambda option: option.option_id)
            satisficing_found = True
        else:
            satisficing = optimizing
            satisficing_found = False

        full_search_cost = len(subset) * subset[0].search_cost_per_option
        optimizing_net_value = optimizing.adjusted_utility - full_search_cost
        opportunity_loss = optimizing.adjusted_utility - satisficing.adjusted_utility
        net_value_advantage = satisficing.net_value - optimizing_net_value

        review = (
            opportunity_loss > 0.20
            or satisficing.option_id > 10
            or not satisficing_found
        )

        output.append({
            "cycle": cycle,
            "domain": subset[0].domain,
            "aspiration": round(subset[0].aspiration, 6),
            "search_cost_per_option": round(subset[0].search_cost_per_option, 6),
            "optimizing_option": optimizing.option_id,
            "optimizing_adjusted_utility": round(optimizing.adjusted_utility, 6),
            "optimizing_net_value": round(optimizing_net_value, 6),
            "satisficing_option": satisficing.option_id,
            "satisficing_adjusted_utility": round(satisficing.adjusted_utility, 6),
            "satisficing_net_value": round(satisficing.net_value, 6),
            "satisficing_found": satisficing_found,
            "search_length": satisficing.option_id,
            "opportunity_loss": round(opportunity_loss, 6),
            "net_value_advantage": round(net_value_advantage, 6),
            "review_flag": "review" if review else "acceptable",
        })

    return output


def group_summary(rows: list[dict[str, object]], field: str) -> list[dict[str, object]]:
    output: list[dict[str, object]] = []

    for group in sorted({row[field] for row in rows}):
        subset = [row for row in rows if row[field] == group]
        output.append({
            field: group,
            "n_cycles": len(subset),
            "average_aspiration": round(mean(float(row["aspiration"]) for row in subset), 6),
            "average_search_length": round(mean(float(row["search_length"]) for row in subset), 6),
            "satisficing_found_rate": round(sum(1 for row in subset if row["satisficing_found"]) / len(subset), 6),
            "average_opportunity_loss": round(mean(float(row["opportunity_loss"]) for row in subset), 6),
            "average_net_value_advantage": round(mean(float(row["net_value_advantage"]) for row in subset), 6),
            "review_rate": round(sum(1 for row in subset if row["review_flag"] == "review") / len(subset), 6),
        })

    return output


def simulate_adaptive_aspiration(n_periods: int = 80, seed: int = 101) -> list[dict[str, object]]:
    rng = random.Random(seed)
    aspiration = 0.70
    learning_rate = 0.12
    search_cost = 0.02
    rows: list[dict[str, object]] = []

    for period in range(1, n_periods + 1):
        options = [clamp(rng.gauss(0.68, 0.13)) for _ in range(10)]
        selected_index = None
        selected_raw_value = None

        for index, value in enumerate(options, start=1):
            if value >= aspiration:
                selected_index = index
                selected_raw_value = value
                break

        if selected_index is None or selected_raw_value is None:
            selected_index, selected_raw_value = max(
                enumerate(options, start=1),
                key=lambda item: item[1],
            )

        selected_net_value = selected_raw_value - selected_index * search_cost
        feedback = selected_net_value + rng.gauss(0.0, 0.03)
        next_aspiration = max(0.35, min(0.95, aspiration + learning_rate * (feedback - aspiration)))

        rows.append({
            "period": period,
            "aspiration": round(aspiration, 6),
            "selected_raw_value": round(selected_raw_value, 6),
            "selected_net_value": round(selected_net_value, 6),
            "search_length": selected_index,
            "feedback": round(feedback, 6),
            "next_aspiration": round(next_aspiration, 6),
        })

        aspiration = next_aspiration

    return rows


def overall_metrics(cycle_rows: list[dict[str, object]], aspiration_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {"metric": "average_search_length", "value": round(mean(float(row["search_length"]) for row in cycle_rows), 6)},
        {"metric": "satisficing_found_rate", "value": round(sum(1 for row in cycle_rows if row["satisficing_found"]) / len(cycle_rows), 6)},
        {"metric": "average_opportunity_loss", "value": round(mean(float(row["opportunity_loss"]) for row in cycle_rows), 6)},
        {"metric": "average_net_value_advantage", "value": round(mean(float(row["net_value_advantage"]) for row in cycle_rows), 6)},
        {"metric": "review_rate", "value": round(sum(1 for row in cycle_rows if row["review_flag"] == "review") / len(cycle_rows), 6)},
        {"metric": "final_adaptive_aspiration", "value": aspiration_rows[-1]["next_aspiration"]},
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
    options = generate_option_search_cases()
    option_output = option_rows(options)
    cycle_rows = cycle_summary(options)
    domain_rows = group_summary(cycle_rows, "domain")
    aspiration_rows = simulate_adaptive_aspiration()
    metric_rows = overall_metrics(cycle_rows, aspiration_rows)
    review_rows = [row for row in cycle_rows if row["review_flag"] == "review"]

    write_csv(TABLES / "bounded_rationality_option_search_cases.csv", option_output)
    write_csv(TABLES / "bounded_rationality_cycle_summary.csv", cycle_rows)
    write_csv(TABLES / "domain_bounded_rationality_summary.csv", domain_rows)
    write_csv(TABLES / "adaptive_aspiration_path.csv", aspiration_rows)
    write_csv(TABLES / "bounded_rationality_review_queue.csv", review_rows)
    write_csv(TABLES / "overall_bounded_rationality_metrics.csv", metric_rows)

    write_json(
        RECORDS / "bounded_rationality_decision_record.json",
        {
            "article": "Bounded Rationality",
            "decision_context": "Comparing optimizing and satisficing rules under search cost, uncertainty penalties, implementation risk, and adaptive aspiration.",
            "modeling_principles": [
                "Decision-makers operate under cognitive, informational, temporal, and institutional constraints.",
                "Alternatives often must be searched for rather than assumed to be fully known.",
                "Satisficing can be reasonable when search is costly and aspiration levels are explicit.",
                "Decision quality depends on search design, stopping rules, and feedback quality.",
                "Decision records should preserve aspiration thresholds, search assumptions, selected alternatives, and review triggers.",
            ],
            "overall_metrics": metric_rows,
            "domain_summary": domain_rows,
            "review_queue_size": len(review_rows),
        },
    )

    print("Bounded rationality workflow complete.")
    print(TABLES / "bounded_rationality_option_search_cases.csv")
    print(TABLES / "bounded_rationality_cycle_summary.csv")
    print(TABLES / "domain_bounded_rationality_summary.csv")
    print(TABLES / "adaptive_aspiration_path.csv")
    print(RECORDS / "bounded_rationality_decision_record.json")


if __name__ == "__main__":
    main()
