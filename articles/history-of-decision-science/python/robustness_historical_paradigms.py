#!/usr/bin/env python3
"""Robustness comparison across historical paradigms."""

from __future__ import annotations


def robustness(payoffs: list[float], threshold: float) -> float:
    return sum(1 for payoff in payoffs if payoff >= threshold) / len(payoffs)


if __name__ == "__main__":
    matrix = {
        "Aggressive": [128, 50, -90, -20],
        "Balanced": [92, 68, 18, 42],
        "Defensive": [62, 58, 44, 54],
        "Adaptive": [88, 70, 36, 72],
    }
    print({name: robustness(values, 40) for name, values in matrix.items()})
