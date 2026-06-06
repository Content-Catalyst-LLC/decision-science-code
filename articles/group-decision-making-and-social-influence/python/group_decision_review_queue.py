#!/usr/bin/env python3
"""Group decision review queue helper."""

from __future__ import annotations


def review_flag(
    collective_error: float,
    social_influence_error_change: float,
    influence_concentration: float,
    hidden_profile_risk: float,
    consensus_pressure: float,
) -> str:
    if (
        collective_error > 0.15
        or social_influence_error_change > 0.05
        or influence_concentration > 0.35
        or hidden_profile_risk > 0.45
        or consensus_pressure > 0.60
    ):
        return "review"
    return "acceptable"


if __name__ == "__main__":
    print(review_flag(0.10, 0.02, 0.30, 0.40, 0.50))
    print(review_flag(0.10, 0.02, 0.30, 0.50, 0.50))
