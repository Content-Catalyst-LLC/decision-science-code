#!/usr/bin/env python3
"""Maximin decision rule helper."""

from __future__ import annotations


def maximin_value(values: list[float]) -> float:
    if not values:
        raise ValueError("At least one value is required.")
    return min(values)


if __name__ == "__main__":
    print(round(maximin_value([0.73, 0.81, 0.79]), 6))
