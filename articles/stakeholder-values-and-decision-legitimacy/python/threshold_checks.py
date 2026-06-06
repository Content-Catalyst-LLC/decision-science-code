#!/usr/bin/env python3
"""Stakeholder threshold helper."""

from __future__ import annotations


def threshold_pass_rate(values: list[float], thresholds: list[float]) -> float:
    if len(values) != len(thresholds):
        raise ValueError("Values and thresholds must have the same length.")
    return sum(1 for value, threshold in zip(values, thresholds) if value >= threshold) / len(values)


if __name__ == "__main__":
    print(round(threshold_pass_rate([0.70, 0.74, 0.66], [0.66, 0.68, 0.64]), 6))
