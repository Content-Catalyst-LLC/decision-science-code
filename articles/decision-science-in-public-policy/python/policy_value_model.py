#!/usr/bin/env python3
"""Public policy value score helper."""

from __future__ import annotations


def policy_value_score(
    efficiency: float,
    equity: float,
    resilience: float,
    feasibility: float,
    legitimacy: float,
    implementation_capacity: float,
) -> float:
    return (
        0.18 * efficiency
        + 0.22 * equity
        + 0.18 * resilience
        + 0.14 * feasibility
        + 0.14 * legitimacy
        + 0.14 * implementation_capacity
    )


if __name__ == "__main__":
    print(round(policy_value_score(0.72, 0.84, 0.70, 0.76, 0.80, 0.86), 6))
