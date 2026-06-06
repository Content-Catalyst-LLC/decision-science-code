#!/usr/bin/env python3
"""Future decision-science maturity helper."""

from __future__ import annotations


def future_maturity_score(
    ai_support: float,
    governance: float,
    uncertainty: float,
    legitimacy: float,
    reproducibility: float,
    systems_awareness: float,
    ethics: float,
    adaptive_capacity: float,
    failure_risk: float,
) -> float:
    score = (
        0.12 * ai_support
        + 0.14 * governance
        + 0.14 * uncertainty
        + 0.12 * legitimacy
        + 0.12 * reproducibility
        + 0.12 * systems_awareness
        + 0.14 * ethics
        + 0.14 * adaptive_capacity
        - 0.14 * failure_risk
    )
    return max(0.0, min(1.0, score))


if __name__ == "__main__":
    print(round(future_maturity_score(0.86, 0.90, 0.88, 0.84, 0.88, 0.86, 0.90, 0.88, 0.24), 6))
