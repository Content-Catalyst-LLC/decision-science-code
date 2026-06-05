#!/usr/bin/env python3
"""Expected loss calculator."""

from __future__ import annotations


def expected_loss(probabilities: list[float], losses: list[float]) -> float:
    if len(probabilities) != len(losses):
        raise ValueError("Probabilities and losses must have the same length.")
    if any(p < 0 or p > 1 for p in probabilities):
        raise ValueError("Probabilities must be between 0 and 1.")
    return sum(p * loss for p, loss in zip(probabilities, losses))


if __name__ == "__main__":
    print(round(expected_loss([0.08, 0.06, 0.03], [0.035, 0.040, 0.075]), 6))
