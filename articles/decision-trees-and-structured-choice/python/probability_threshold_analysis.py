#!/usr/bin/env python3
"""Probability threshold analysis."""

from __future__ import annotations


def threshold_probability(success_payoff: float, failure_payoff: float, target_value: float, cost: float = 0.0, credit: float = 0.0) -> float | None:
    denominator = success_payoff - failure_payoff
    if abs(denominator) < 1e-12:
        return None
    p = (target_value + cost - credit - failure_payoff) / denominator
    if p < 0 or p > 1:
        return None
    return p


if __name__ == "__main__":
    print(round(threshold_probability(125, -35, 60), 4))
