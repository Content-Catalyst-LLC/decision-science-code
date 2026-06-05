#!/usr/bin/env python3
"""Expected utility comparison scaffold."""

from __future__ import annotations

import math


def utility(value: float, risk_aversion: float = 0.018) -> float:
    return 1.0 - math.exp(-risk_aversion * value)


def expected_utility(payoffs: list[float], probabilities: list[float]) -> float:
    if len(payoffs) != len(probabilities):
        raise ValueError("payoffs and probabilities must align")
    return sum(probability * utility(payoff) for payoff, probability in zip(payoffs, probabilities))


if __name__ == "__main__":
    probabilities = [0.22, 0.34, 0.18, 0.16, 0.10]
    strategies = {
        "Optimize": [145, 92, 30, -95, -40],
        "Balanced": [112, 84, 58, 12, 30],
        "Robust": [78, 72, 65, 48, 55],
    }
    for name, payoffs in strategies.items():
        print(name, round(expected_utility(payoffs, probabilities), 6))
