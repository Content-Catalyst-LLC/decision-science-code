#!/usr/bin/env python3
"""Robustness threshold diagnostics."""

from __future__ import annotations


def robustness_share(payoffs: list[float], threshold: float) -> float:
    return sum(1 for payoff in payoffs if payoff >= threshold) / len(payoffs)


if __name__ == "__main__":
    matrix = {
        "Expand": [120, 45, -95, -130, 20],
        "Hedge": [92, 68, 18, -20, 55],
        "Preserve Option": [72, 62, 42, 18, 70],
        "Adaptive Pathway": [95, 72, 34, 10, 78],
    }
    print({name: robustness_share(values, 40) for name, values in matrix.items()})
