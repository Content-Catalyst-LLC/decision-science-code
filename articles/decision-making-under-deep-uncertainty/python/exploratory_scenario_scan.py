#!/usr/bin/env python3
"""Exploratory scenario scan helper."""

from __future__ import annotations


def scenario_spread(values: list[float]) -> float:
    if not values:
        raise ValueError("At least one value is required.")
    return max(values) - min(values)


if __name__ == "__main__":
    print(round(scenario_spread([0.91, 0.31, 0.18, 0.52]), 6))
