#!/usr/bin/env python3
"""Maximin helper for scenario evaluation."""

from __future__ import annotations


def worst_case(values: list[float]) -> float:
    if not values:
        raise ValueError("At least one value is required.")
    return min(values)


if __name__ == "__main__":
    print(round(worst_case([0.78, 0.76, 0.82, 0.80]), 6))
