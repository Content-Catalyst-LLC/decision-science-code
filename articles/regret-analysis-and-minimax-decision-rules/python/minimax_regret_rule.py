#!/usr/bin/env python3
"""Minimax regret decision rule helper."""

from __future__ import annotations


def maximum_regret(values: list[float]) -> float:
    if not values:
        raise ValueError("At least one regret value is required.")
    return max(values)


if __name__ == "__main__":
    print(round(maximum_regret([0.19, 0.00, 0.05]), 6))
