#!/usr/bin/env python3
"""Subjective expected utility model."""

from __future__ import annotations

import math


def utility(value: float, risk_aversion: float = 0.016) -> float:
    return 1.0 - math.exp(-risk_aversion * value)


def subjective_expected_utility(payoffs: list[float], beliefs: list[float]) -> float:
    return sum(utility(x) * p for x, p in zip(payoffs, beliefs))


if __name__ == "__main__":
    subjective_beliefs = [0.30, 0.34, 0.24, 0.12]
    print(subjective_expected_utility([88, 70, 36, 72], subjective_beliefs))
