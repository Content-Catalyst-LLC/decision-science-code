#!/usr/bin/env python3
"""
Bayesian Decision-Making Simulation

Computes Bayesian updates, posterior odds, Bayes factors,
posterior expected utilities, prior sensitivity, sequential evidence
updates, review triggers, and a decision-record JSON file.

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


@dataclass(frozen=True)
class BayesianCase:
    name: str
    prior: float
    sensitivity: float
    false_positive_rate: float
    action_success_utility: float
    action_false_positive_cost: float
    inaction_miss_cost: float
    inaction_true_negative_utility: float
    description: str


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def load_cases() -> list[BayesianCase]:
    rows = read_csv_dicts(DATA / "synthetic_bayesian_cases.csv")
    return [
        BayesianCase(
            row["case"],
            float(row["prior"]),
            float(row["sensitivity"]),
            float(row["false_positive_rate"]),
            float(row["action_success_utility"]),
            float(row["action_false_positive_cost"]),
            float(row["inaction_miss_cost"]),
            float(row["inaction_true_negative_utility"]),
            row["description"],
        )
        for row in rows
    ]


def bayesian_update_positive(prior: float, sensitivity: float, false_positive_rate: float) -> float:
    numerator = sensitivity * prior
    denominator = numerator + false_positive_rate * (1.0 - prior)
    if denominator == 0:
        raise ValueError("Evidence probability is zero.")
    return numerator / denominator


def bayesian_update_negative(prior: float, sensitivity: float, false_positive_rate: float) -> float:
    likelihood_negative_given_h = 1.0 - sensitivity
    likelihood_negative_given_not_h = 1.0 - false_positive_rate
    numerator = likelihood_negative_given_h * prior
    denominator = numerator + likelihood_negative_given_not_h * (1.0 - prior)
    if denominator == 0:
        raise ValueError("Evidence probability is zero.")
    return numerator / denominator


def posterior_odds(posterior: float) -> float:
    if posterior >= 1.0:
        return float("inf")
    if posterior <= 0.0:
        return 0.0
    return posterior / (1.0 - posterior)


def bayes_factor(sensitivity: float, false_positive_rate: float) -> float:
    if false_positive_rate == 0:
        return float("inf")
    return sensitivity / false_positive_rate


def action_utility(posterior: float, case: BayesianCase) -> float:
    return posterior * case.action_success_utility + (1.0 - posterior) * case.action_false_positive_cost


def wait_utility(posterior: float, case: BayesianCase) -> float:
    return posterior * case.inaction_miss_cost + (1.0 - posterior) * case.inaction_true_negative_utility


def case_profiles(cases: list[BayesianCase]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    for case in cases:
        posterior = bayesian_update_positive(case.prior, case.sensitivity, case.false_positive_rate)
        act_u = action_utility(posterior, case)
        wait_u = wait_utility(posterior, case)
        utility_difference = act_u - wait_u

        rows.append({
            "case": case.name,
            "description": case.description,
            "prior": round(case.prior, 6),
            "sensitivity": round(case.sensitivity, 6),
            "false_positive_rate": round(case.false_positive_rate, 6),
            "bayes_factor_positive": round(bayes_factor(case.sensitivity, case.false_positive_rate), 6),
            "posterior_after_positive_signal": round(posterior, 6),
            "posterior_odds": round(posterior_odds(posterior), 6),
            "action_utility": round(act_u, 6),
            "wait_utility": round(wait_u, 6),
            "utility_difference": round(utility_difference, 6),
            "recommended_action": "Act" if utility_difference >= 0 else "Wait or gather more evidence",
            "posterior_review_flag": "decision-sensitive: review assumptions" if abs(utility_difference) < 10 else "stable under baseline assumptions",
        })

    return rows


def simulate_evidence_stream(case: BayesianCase, steps: int, true_state: bool, seed: int) -> list[dict[str, object]]:
    rng = random.Random(seed)
    posterior = case.prior
    rows: list[dict[str, object]] = []

    for step in range(1, steps + 1):
        if true_state:
            positive_signal = rng.random() < case.sensitivity
        else:
            positive_signal = rng.random() < case.false_positive_rate

        prior_before_update = posterior

        if positive_signal:
            posterior = bayesian_update_positive(posterior, case.sensitivity, case.false_positive_rate)
        else:
            posterior = bayesian_update_negative(posterior, case.sensitivity, case.false_positive_rate)

        act_u = action_utility(posterior, case)
        wait_u = wait_utility(posterior, case)
        utility_difference = act_u - wait_u
        action = "Act" if utility_difference >= 0 else "Wait"

        review_trigger = (
            posterior >= 0.70
            or abs(utility_difference) < 8.0
            or (action == "Wait" and posterior >= 0.45)
        )

        rows.append({
            "case": case.name,
            "step": step,
            "true_state": true_state,
            "positive_signal": positive_signal,
            "prior_before_update": round(prior_before_update, 6),
            "posterior": round(posterior, 6),
            "posterior_odds": round(posterior_odds(posterior), 6),
            "action_utility": round(act_u, 6),
            "wait_utility": round(wait_u, 6),
            "utility_difference": round(utility_difference, 6),
            "recommended_action": action,
            "review_trigger": review_trigger,
        })

    return rows


def summarize_sequential(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    cases = sorted({str(row["case"]) for row in rows})
    output: list[dict[str, object]] = []

    for case in cases:
        subset = [row for row in rows if row["case"] == case]
        posteriors = [float(row["posterior"]) for row in subset]
        utility_differences = [float(row["utility_difference"]) for row in subset]
        triggers = [bool(row["review_trigger"]) for row in subset]
        final_row = max(subset, key=lambda row: int(row["step"]))

        output.append({
            "case": case,
            "initial_posterior": round(posteriors[0], 6),
            "final_posterior": round(posteriors[-1], 6),
            "average_posterior": round(mean(posteriors), 6),
            "maximum_posterior": round(max(posteriors), 6),
            "minimum_posterior": round(min(posteriors), 6),
            "average_utility_difference": round(mean(utility_differences), 6),
            "final_recommended_action": final_row["recommended_action"],
            "review_trigger_rate": round(sum(1 for item in triggers if item) / len(triggers), 6),
        })

    return output


def prior_sensitivity(case: BayesianCase) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    for i in range(1, 91):
        prior = i / 100
        posterior = bayesian_update_positive(prior, case.sensitivity, case.false_positive_rate)
        act_u = action_utility(posterior, case)
        wait_u = wait_utility(posterior, case)

        rows.append({
            "case": case.name,
            "prior": round(prior, 4),
            "posterior_after_positive_signal": round(posterior, 6),
            "action_utility": round(act_u, 6),
            "wait_utility": round(wait_u, 6),
            "utility_difference": round(act_u - wait_u, 6),
            "recommended_action": "Act" if act_u >= wait_u else "Wait",
        })

    return rows


def value_of_information_proxy(case: BayesianCase) -> dict[str, object]:
    prior_act_u = action_utility(case.prior, case)
    prior_wait_u = wait_utility(case.prior, case)
    baseline = max(prior_act_u, prior_wait_u)

    posterior_positive = bayesian_update_positive(case.prior, case.sensitivity, case.false_positive_rate)
    posterior_negative = bayesian_update_negative(case.prior, case.sensitivity, case.false_positive_rate)

    p_positive = case.sensitivity * case.prior + case.false_positive_rate * (1.0 - case.prior)
    p_negative = 1.0 - p_positive

    utility_after_positive = max(action_utility(posterior_positive, case), wait_utility(posterior_positive, case))
    utility_after_negative = max(action_utility(posterior_negative, case), wait_utility(posterior_negative, case))

    expected_utility_with_signal = p_positive * utility_after_positive + p_negative * utility_after_negative
    evsi = expected_utility_with_signal - baseline

    return {
        "case": case.name,
        "baseline_best_utility": round(baseline, 6),
        "expected_utility_with_signal": round(expected_utility_with_signal, 6),
        "expected_value_of_sample_information_proxy": round(evsi, 6),
    }


def evidence_quality_summary() -> list[dict[str, object]]:
    quality_map = {"high": 1.0, "medium": 0.65, "low": 0.35}
    rows = read_csv_dicts(DATA / "synthetic_likelihoods.csv")
    output = []

    for row in rows:
        score = quality_map.get(row["evidence_quality"].lower(), 0.0)
        output.append({
            "case": row["case"],
            "evidence": row["evidence"],
            "sensitivity": float(row["sensitivity"]),
            "false_positive_rate": float(row["false_positive_rate"]),
            "evidence_quality": row["evidence_quality"],
            "evidence_quality_score": score,
            "quality_flag": "review" if score < 0.60 else "acceptable",
        })

    return output


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
    cases = load_cases()

    profiles = case_profiles(cases)

    all_updates: list[dict[str, object]] = []
    for index, case in enumerate(cases):
        true_state = index % 2 == 0
        all_updates.extend(simulate_evidence_stream(case, steps=24, true_state=true_state, seed=42 + index))

    sensitivity_rows: list[dict[str, object]] = []
    for case in cases:
        sensitivity_rows.extend(prior_sensitivity(case))

    summary_rows = summarize_sequential(all_updates)
    evsi_rows = [value_of_information_proxy(case) for case in cases]
    quality_rows = evidence_quality_summary()

    write_csv(TABLES / "bayesian_decision_profiles.csv", profiles)
    write_csv(TABLES / "bayesian_sequential_updates.csv", all_updates)
    write_csv(TABLES / "bayesian_decision_summary.csv", summary_rows)
    write_csv(TABLES / "bayesian_prior_sensitivity.csv", sensitivity_rows)
    write_csv(TABLES / "bayesian_value_of_information_proxy.csv", evsi_rows)
    write_csv(TABLES / "bayesian_evidence_quality_summary.csv", quality_rows)

    write_json(
        RECORDS / "bayesian_decision_record.json",
        {
            "article": "Bayesian Decision-Making",
            "decision_context": "Sequential belief updating and action selection under uncertainty.",
            "modeling_principles": [
                "Document the prior before observing new evidence.",
                "Represent evidence strength through likelihoods.",
                "Update beliefs using Bayes' theorem.",
                "Evaluate actions under posterior expected utility.",
                "Use sensitivity analysis when priors or likelihoods are contested.",
                "Define review triggers when posterior beliefs cross decision thresholds.",
                "Treat Bayesian models as supports for accountable judgment.",
            ],
            "case_profiles": profiles,
            "summary": summary_rows,
            "value_of_information_proxy": evsi_rows,
            "evidence_quality": quality_rows,
        },
    )

    print("Bayesian decision-making workflow complete.")
    print(TABLES / "bayesian_decision_profiles.csv")
    print(TABLES / "bayesian_sequential_updates.csv")
    print(TABLES / "bayesian_decision_summary.csv")
    print(TABLES / "bayesian_prior_sensitivity.csv")
    print(TABLES / "bayesian_value_of_information_proxy.csv")
    print(TABLES / "bayesian_evidence_quality_summary.csv")
    print(RECORDS / "bayesian_decision_record.json")


if __name__ == "__main__":
    main()
