#!/usr/bin/env python3
"""Decision-change probability helper."""

from __future__ import annotations


def decision_change_probability(probabilities: list[float], changes: list[bool]) -> float:
    if len(probabilities) != len(changes):
        raise ValueError("Probabilities and change flags must have the same length.")
    return sum(probability for probability, changed in zip(probabilities, changes) if changed)


if __name__ == "__main__":
    print(round(decision_change_probability([0.4, 0.35, 0.25], [False, True, True]), 6))
