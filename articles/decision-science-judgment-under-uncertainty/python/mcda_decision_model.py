"""
Decision Science: Multi-Criteria Decision Analysis in Python

Educational workflow for comparing alternatives across multiple criteria.
"""

from __future__ import annotations

import pandas as pd


WEIGHTS = {
    "cost_efficiency": 0.16,
    "effectiveness": 0.22,
    "equity": 0.18,
    "feasibility": 0.16,
    "resilience": 0.20,
    "implementation_risk": -0.08
}


def weighted_score(row: pd.Series) -> float:
    """Compute weighted MCDA score."""
    return sum(row[criterion] * weight for criterion, weight in WEIGHTS.items())


def main() -> None:
    alternatives = pd.read_csv("../data/decision_alternatives.csv")
    alternatives["decision_score"] = alternatives.apply(weighted_score, axis=1)

    alternatives["requires_deliberation"] = (
        (alternatives["implementation_risk"] > 0.55)
        | (alternatives["equity"] < 0.60)
        | (alternatives["resilience"] < 0.60)
    )

    alternatives = alternatives.sort_values("decision_score", ascending=False)

    print(alternatives)

    alternatives.to_csv("../outputs/mcda_decision_scores.csv", index=False)


if __name__ == "__main__":
    main()
