#!/usr/bin/env python3
"""Scenario dispersion helper."""

from __future__ import annotations

from statistics import pstdev


def scenario_dispersion(values: list[float]) -> float:
    if not values:
        raise ValueError("At least one value is required.")
    return pstdev(values)


if __name__ == "__main__":
    print(round(scenario_dispersion([0.78, 0.76, 0.82, 0.80]), 6))
