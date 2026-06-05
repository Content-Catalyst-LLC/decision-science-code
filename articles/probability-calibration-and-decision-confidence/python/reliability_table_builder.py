#!/usr/bin/env python3
"""Reliability table mini-example."""

from __future__ import annotations

from statistics import mean


def calibration_gap(probabilities: list[float], outcomes: list[int]) -> float:
    if len(probabilities) != len(outcomes):
        raise ValueError("Probabilities and outcomes must have the same length.")
    return mean(probabilities) - mean(outcomes)


if __name__ == "__main__":
    print(round(calibration_gap([0.72, 0.76, 0.79], [1, 1, 0]), 6))
