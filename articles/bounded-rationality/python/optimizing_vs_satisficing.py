#!/usr/bin/env python3
"""Optimization benchmark versus satisficing helper."""

from __future__ import annotations


def optimizing_choice(values: list[float]) -> tuple[int, float]:
    index, value = max(enumerate(values, start=1), key=lambda item: item[1])
    return index, value


def opportunity_loss(values: list[float], selected_index: int) -> float:
    _, best = optimizing_choice(values)
    return best - values[selected_index - 1]


if __name__ == "__main__":
    values = [0.58, 0.71, 0.82, 0.77, 0.91]
    print(optimizing_choice(values))
    print(round(opportunity_loss(values, 3), 6))
