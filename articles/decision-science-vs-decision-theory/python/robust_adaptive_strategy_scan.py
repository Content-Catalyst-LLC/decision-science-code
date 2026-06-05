#!/usr/bin/env python3
"""Robust adaptive strategy scan."""

from __future__ import annotations


def robustness(payoffs: list[float], threshold: float) -> float:
    return sum(1 for value in payoffs if value >= threshold) / len(payoffs)


if __name__ == "__main__":
    matrix = {
        "Optimize": [145, 92, 30, -95, -40],
        "Balanced": [112, 84, 58, 12, 30],
        "Robust": [78, 72, 65, 48, 55],
        "Adaptive": [98, 80, 62, 38, 68],
        "Staged Pilot": [82, 70, 60, 42, 74],
    }
    scores = {name: robustness(values, threshold=45) for name, values in matrix.items()}
    print(scores)
    print("Most robust:", max(scores, key=scores.get))
