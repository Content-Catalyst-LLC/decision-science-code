#!/usr/bin/env python3
"""
Value of Information and When to Wait workflow.

Calculates current expected value, expected value of perfect information,
expected value of sample information, decision-change probability, net
value of information, net value of waiting, timing recommendation, and
decision-record export.

Uses only the Python standard library.
"""

from __future__ import annotations

from pathlib import Path
import csv
import json

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
DATA = ARTICLE_ROOT / "data"
TABLES = ARTICLE_ROOT / "outputs" / "tables"
RECORDS = ARTICLE_ROOT / "outputs" / "decision_records"


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def load_states() -> list[str]:
    return [row["state"] for row in read_csv_dicts(DATA / "synthetic_states.csv")]


def load_prior_probabilities() -> dict[str, float]:
    probabilities = {
        row["state"]: float(row["probability"])
        for row in read_csv_dicts(DATA / "synthetic_prior_probabilities.csv")
    }
    ensure_probabilities(probabilities, "Prior")
    return probabilities


def load_payoff_matrix() -> list[dict[str, object]]:
    states = load_states()
    rows = read_csv_dicts(DATA / "synthetic_payoff_matrix.csv")
    output: list[dict[str, object]] = []
    for row in rows:
        item: dict[str, object] = {"action": row["action"]}
        for state in states:
            item[state] = float(row[state])
        output.append(item)
    return output


def load_evidence_model() -> tuple[dict[str, float], dict[str, dict[str, float]]]:
    rows = read_csv_dicts(DATA / "synthetic_evidence_posteriors.csv")
    evidence_names = sorted({row["evidence"] for row in rows})
    evidence_probabilities: dict[str, float] = {}
    posteriors: dict[str, dict[str, float]] = {}

    for evidence in evidence_names:
        subset = [row for row in rows if row["evidence"] == evidence]
        evidence_probabilities[evidence] = float(subset[0]["evidence_probability"])
        posteriors[evidence] = {
            row["state"]: float(row["posterior_probability"])
            for row in subset
        }
        ensure_probabilities(posteriors[evidence], evidence)

    ensure_probabilities(evidence_probabilities, "Evidence")
    return evidence_probabilities, posteriors


def load_costs() -> dict[str, float]:
    return {
        row["cost_name"]: float(row["value"])
        for row in read_csv_dicts(DATA / "synthetic_information_costs.csv")
    }


def ensure_probabilities(probabilities: dict[str, float], label: str) -> None:
    total = sum(probabilities.values())
    if abs(total - 1.0) > 1e-6:
        raise ValueError(f"{label} probabilities must sum to 1. Got {total}.")


def expected_value(action: dict[str, object], probabilities: dict[str, float], states: list[str]) -> float:
    return sum(float(action[state]) * probabilities[state] for state in states)


def best_action(actions: list[dict[str, object]], probabilities: dict[str, float], states: list[str]) -> tuple[str, float]:
    values = [
        (str(action["action"]), expected_value(action, probabilities, states))
        for action in actions
    ]
    return max(values, key=lambda item: item[1])


def expected_value_with_perfect_information(
    actions: list[dict[str, object]],
    prior_probabilities: dict[str, float],
    states: list[str],
) -> float:
    total = 0.0
    for state, probability in prior_probabilities.items():
        best_payoff_for_state = max(float(action[state]) for action in actions)
        total += probability * best_payoff_for_state
    return total


def sample_information_results(
    actions: list[dict[str, object]],
    current_action: str,
    evidence_probabilities: dict[str, float],
    posteriors: dict[str, dict[str, float]],
    states: list[str],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    for evidence, signal_probability in evidence_probabilities.items():
        posterior = posteriors[evidence]
        action_after_evidence, value_after_evidence = best_action(actions, posterior, states)

        rows.append({
            "evidence": evidence,
            "evidence_probability": round(signal_probability, 6),
            "best_action_after_evidence": action_after_evidence,
            "expected_value_after_evidence": round(value_after_evidence, 6),
            "decision_changes": action_after_evidence != current_action,
        })

    return rows


def timing_recommendation(net_value_waiting: float, net_value_information: float, evsi: float, delay_cost: float) -> str:
    if net_value_waiting > 0:
        return "wait_for_information"
    if net_value_information > 0 and delay_cost > evsi * 0.5:
        return "learn_while_acting"
    return "act_now_or_stage"


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
    states = load_states()
    actions = load_payoff_matrix()
    prior_probabilities = load_prior_probabilities()
    evidence_probabilities, posteriors = load_evidence_model()
    costs = load_costs()

    information_cost = costs["information_cost"]
    delay_cost = costs["delay_cost"]

    current_action, current_expected_value = best_action(actions, prior_probabilities, states)
    ev_perfect = expected_value_with_perfect_information(actions, prior_probabilities, states)
    evpi = ev_perfect - current_expected_value

    sample_rows = sample_information_results(
        actions,
        current_action,
        evidence_probabilities,
        posteriors,
        states,
    )

    ev_sample = sum(
        evidence_probabilities[str(row["evidence"])] * float(row["expected_value_after_evidence"])
        for row in sample_rows
    )

    evsi = ev_sample - current_expected_value
    net_value_information = evsi - information_cost
    net_value_waiting = evsi - information_cost - delay_cost

    decision_change_probability = sum(
        evidence_probabilities[str(row["evidence"])] * (1.0 if row["decision_changes"] else 0.0)
        for row in sample_rows
    )

    recommendation = timing_recommendation(net_value_waiting, net_value_information, evsi, delay_cost)

    current_expected_value_rows = [
        {
            "action": str(action["action"]),
            "current_expected_value": round(expected_value(action, prior_probabilities, states), 6),
        }
        for action in actions
    ]

    prior_rows = [
        {"state": state, "probability": probability}
        for state, probability in prior_probabilities.items()
    ]

    posterior_rows = [
        {"evidence": evidence, "state": state, "posterior_probability": probability}
        for evidence, posterior in posteriors.items()
        for state, probability in posterior.items()
    ]

    summary_rows = [
        {"metric": "current_best_action", "value": current_action},
        {"metric": "current_expected_value", "value": round(current_expected_value, 6)},
        {"metric": "expected_value_with_perfect_information", "value": round(ev_perfect, 6)},
        {"metric": "expected_value_of_perfect_information", "value": round(evpi, 6)},
        {"metric": "expected_value_with_sample_information", "value": round(ev_sample, 6)},
        {"metric": "expected_value_of_sample_information", "value": round(evsi, 6)},
        {"metric": "information_cost", "value": information_cost},
        {"metric": "delay_cost", "value": delay_cost},
        {"metric": "net_value_of_information", "value": round(net_value_information, 6)},
        {"metric": "net_value_of_waiting", "value": round(net_value_waiting, 6)},
        {"metric": "decision_change_probability", "value": round(decision_change_probability, 6)},
        {"metric": "recommendation", "value": recommendation},
    ]

    timing_rows = [{
        "current_best_action": current_action,
        "evpi": round(evpi, 6),
        "evsi": round(evsi, 6),
        "information_cost": information_cost,
        "delay_cost": delay_cost,
        "net_value_information": round(net_value_information, 6),
        "net_value_waiting": round(net_value_waiting, 6),
        "decision_change_probability": round(decision_change_probability, 6),
        "recommendation": recommendation,
    }]

    write_csv(TABLES / "voi_payoff_matrix.csv", actions)
    write_csv(TABLES / "voi_prior_probabilities.csv", prior_rows)
    write_csv(TABLES / "voi_posterior_probabilities_by_evidence.csv", posterior_rows)
    write_csv(TABLES / "voi_current_expected_values.csv", current_expected_value_rows)
    write_csv(TABLES / "voi_sample_information_results.csv", sample_rows)
    write_csv(TABLES / "voi_summary_metrics.csv", summary_rows)
    write_csv(TABLES / "voi_timing_recommendation.csv", timing_rows)

    write_json(
        RECORDS / "value_of_information_decision_record.json",
        {
            "article": "Value of Information and When to Wait",
            "decision_context": "Comparing action now, waiting, piloting, staging, and monitoring using value of information and delay cost.",
            "states": states,
            "prior_probabilities": prior_probabilities,
            "evidence_probabilities": evidence_probabilities,
            "posteriors": posteriors,
            "information_cost": information_cost,
            "delay_cost": delay_cost,
            "current_best_action": current_action,
            "evpi": evpi,
            "evsi": evsi,
            "net_value_information": net_value_information,
            "net_value_waiting": net_value_waiting,
            "decision_change_probability": decision_change_probability,
            "recommendation": recommendation,
            "modeling_principles": [
                "Information has value only when it can improve a decision.",
                "EVPI provides an upper bound on information value.",
                "EVSI evaluates imperfect evidence such as studies, pilots, tests, and monitoring.",
                "Net value of waiting subtracts both information cost and delay cost.",
                "When delay is costly, staged action or learning while acting may dominate waiting."
            ],
        },
    )

    print("Value of information and waiting workflow complete.")
    print(TABLES / "voi_summary_metrics.csv")
    print(TABLES / "voi_timing_recommendation.csv")
    print(RECORDS / "value_of_information_decision_record.json")


if __name__ == "__main__":
    main()
