#!/usr/bin/env python3
"""Forecast error metric helpers."""

from __future__ import annotations

import math


def mean_absolute_error(actual: list[float], forecast: list[float]) -> float:
    if len(actual) != len(forecast):
        raise ValueError("Actual and forecast lists must have the same length.")
    return sum(abs(a - f) for a, f in zip(actual, forecast)) / len(actual)


def root_mean_squared_error(actual: list[float], forecast: list[float]) -> float:
    if len(actual) != len(forecast):
        raise ValueError("Actual and forecast lists must have the same length.")
    return math.sqrt(sum((a - f) ** 2 for a, f in zip(actual, forecast)) / len(actual))


if __name__ == "__main__":
    actual_values = [100.0, 112.0, 95.0, 121.0]
    forecast_values = [98.0, 108.0, 101.0, 119.0]
    print(round(mean_absolute_error(actual_values, forecast_values), 6))
    print(round(root_mean_squared_error(actual_values, forecast_values), 6))
