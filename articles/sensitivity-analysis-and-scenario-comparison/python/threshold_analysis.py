#!/usr/bin/env python3
"""Threshold analysis helper."""

from __future__ import annotations


def threshold_for_equal_utility(a_intercept: float, a_slope: float, b_intercept: float, b_slope: float) -> float | None:
    denominator = a_slope - b_slope
    if abs(denominator) < 1e-12:
        return None
    return (b_intercept - a_intercept) / denominator


if __name__ == "__main__":
    print(threshold_for_equal_utility(70.0, 5.5, 73.0, 7.0))
