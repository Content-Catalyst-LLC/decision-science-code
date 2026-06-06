#!/usr/bin/env python3
"""Public trust dynamics helper."""

from __future__ import annotations


def next_trust(
    current_trust: float,
    performance: float,
    transparency: float,
    responsiveness: float,
    fairness: float,
    uncertainty_stress: float,
    harm: float,
) -> float:
    trust = (
        current_trust
        + 0.08 * performance
        + 0.06 * transparency
        + 0.08 * responsiveness
        + 0.08 * fairness
        - 0.06 * uncertainty_stress
        - 0.10 * harm
    )
    return max(0.0, min(1.0, trust))


if __name__ == "__main__":
    print(round(next_trust(0.62, 0.70, 0.78, 0.74, 0.72, 0.36, 0.30), 6))
