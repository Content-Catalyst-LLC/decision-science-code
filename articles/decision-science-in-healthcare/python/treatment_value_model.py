#!/usr/bin/env python3
"""Treatment value score helper."""

from __future__ import annotations


def treatment_value_score(
    expected_benefit: float,
    adverse_event_risk: float,
    cost_burden: float,
    patient_preference_fit: float,
    equity_score: float,
    implementation_feasibility: float,
) -> float:
    return (
        0.30 * expected_benefit
        - 0.18 * adverse_event_risk
        - 0.14 * cost_burden
        + 0.18 * patient_preference_fit
        + 0.10 * equity_score
        + 0.10 * implementation_feasibility
    )


if __name__ == "__main__":
    print(round(treatment_value_score(0.72, 0.12, 0.54, 0.88, 0.76, 0.70), 6))
