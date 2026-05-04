"""
Decision Science: Expected Value, Regret, and Robustness

Educational workflow for comparing decisions through expected value,
scenario robustness, and regret.
"""

from __future__ import annotations

import pandas as pd


def compute_expected_values(outcomes: pd.DataFrame) -> pd.DataFrame:
    """Compute expected value by alternative."""
    return (
        outcomes.assign(weighted_value=outcomes["probability"] * outcomes["value"])
        .groupby("alternative", as_index=False)["weighted_value"]
        .sum()
        .rename(columns={"weighted_value": "expected_value"})
        .sort_values("expected_value", ascending=False)
    )


def compute_robustness(scenario_values: pd.DataFrame) -> pd.DataFrame:
    """Compute worst-case performance across scenarios."""
    return (
        scenario_values.groupby("alternative", as_index=False)["value"]
        .min()
        .rename(columns={"value": "worst_case_value"})
        .sort_values("worst_case_value", ascending=False)
    )


def compute_regret(scenario_values: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Compute regret table and maximum regret by alternative."""
    best_by_scenario = (
        scenario_values.groupby("scenario", as_index=False)["value"]
        .max()
        .rename(columns={"value": "best_value_in_scenario"})
    )

    regret = scenario_values.merge(best_by_scenario, on="scenario", how="left")
    regret["regret"] = regret["best_value_in_scenario"] - regret["value"]

    max_regret = (
        regret.groupby("alternative", as_index=False)["regret"]
        .max()
        .rename(columns={"regret": "maximum_regret"})
        .sort_values("maximum_regret", ascending=True)
    )

    return regret, max_regret


def main() -> None:
    outcomes = pd.read_csv("../data/expected_value_inputs.csv")
    scenario_values = pd.read_csv("../data/scenario_values.csv")

    expected_values = compute_expected_values(outcomes)
    robustness = compute_robustness(scenario_values)
    regret, max_regret = compute_regret(scenario_values)

    summary = (
        expected_values
        .merge(robustness, on="alternative", how="outer")
        .merge(max_regret, on="alternative", how="outer")
    )

    summary["decision_support_score"] = (
        0.45 * summary["expected_value"]
        + 0.40 * summary["worst_case_value"]
        - 0.15 * summary["maximum_regret"]
    )

    summary = summary.sort_values("decision_support_score", ascending=False)

    print(summary)

    expected_values.to_csv("../outputs/expected_values.csv", index=False)
    robustness.to_csv("../outputs/robustness_summary.csv", index=False)
    regret.to_csv("../outputs/regret_table.csv", index=False)
    summary.to_csv("../outputs/decision_support_summary.csv", index=False)


if __name__ == "__main__":
    main()
