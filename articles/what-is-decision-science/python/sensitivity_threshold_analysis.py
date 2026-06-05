#!/usr/bin/env python3
"""Threshold and sensitivity analysis scaffold."""

from __future__ import annotations


def threshold_crossings(values: dict[str, float], threshold: float) -> dict[str, bool]:
    return {name: value >= threshold for name, value in values.items()}


def one_way_weight_sensitivity(base_weight: float, deltas: list[float]) -> list[float]:
    return [max(0.0, min(1.0, base_weight + delta)) for delta in deltas]


if __name__ == "__main__":
    scores = {"A": 0.72, "B": 0.64, "C": 0.81}
    print(threshold_crossings(scores, 0.70))
    print(one_way_weight_sensitivity(0.25, [-0.10, -0.05, 0.05, 0.10]))
