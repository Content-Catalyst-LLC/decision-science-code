#!/usr/bin/env python3
"""Criteria normalization helpers."""

from __future__ import annotations


def normalize_benefit(values: list[float]) -> list[float]:
    low = min(values)
    high = max(values)
    if high == low:
        return [1.0 for _ in values]
    return [(value - low) / (high - low) for value in values]


def normalize_cost(values: list[float]) -> list[float]:
    low = min(values)
    high = max(values)
    if high == low:
        return [1.0 for _ in values]
    return [(high - value) / (high - low) for value in values]


if __name__ == "__main__":
    print([round(value, 6) for value in normalize_benefit([1, 2, 5])])
    print([round(value, 6) for value in normalize_cost([10, 20, 40])])
