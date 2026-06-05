#!/usr/bin/env python3
"""Expected monetary value historical baseline."""

from __future__ import annotations


def expected_value(payoffs: list[float], probabilities: list[float]) -> float:
    return sum(x * p for x, p in zip(payoffs, probabilities))


if __name__ == "__main__":
    probabilities = [0.42, 0.28, 0.18, 0.12]
    print(expected_value([128, 50, -90, -20], probabilities))
