#!/usr/bin/env python3
"""Expected-value rollback helper."""

from __future__ import annotations


def chance_node_value(outcomes: list[float], probabilities: list[float]) -> float:
    if len(outcomes) != len(probabilities):
        raise ValueError("Outcomes and probabilities must have the same length.")
    if abs(sum(probabilities) - 1.0) > 1e-9:
        raise ValueError("Probabilities must sum to 1.")
    return sum(x * p for x, p in zip(outcomes, probabilities))


if __name__ == "__main__":
    print(round(chance_node_value([125, -35], [0.58, 0.42]), 4))
