#!/usr/bin/env python3
"""Expected utility under measurable risk."""

from __future__ import annotations

import math


def utility(value: float, risk_aversion: float = 0.016) -> float:
    return 1.0 - math.exp(-risk_aversion * value)


def expected_utility(payoffs: list[float], probabilities: list[float]) -> float:
    if len(payoffs) != len(probabilities):
        raise ValueError("payoffs and probabilities must align")
    return sum(p * utility(x) for x, p in zip(payoffs, probabilities))


if __name__ == "__main__":
    probabilities = [0.40, 0.24, 0.16, 0.10, 0.10]
    payoffs = [120, 45, -95, -130, 20]
    print(round(expected_utility(payoffs, probabilities), 6))
