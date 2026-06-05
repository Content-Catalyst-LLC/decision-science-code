#!/usr/bin/env python3
"""Chance node evaluator."""

from __future__ import annotations


def validate_chance_node(probabilities: list[float]) -> bool:
    return all(0 <= p <= 1 for p in probabilities) and abs(sum(probabilities) - 1.0) <= 1e-9


if __name__ == "__main__":
    print(validate_chance_node([0.58, 0.42]))
