#!/usr/bin/env python3
"""Forecast threshold-decision helper."""

from __future__ import annotations


def threshold_from_costs(false_positive_cost: float, false_negative_cost: float) -> float:
    return false_positive_cost / (false_positive_cost + false_negative_cost)


def should_act(forecast_probability: float, false_positive_cost: float, false_negative_cost: float) -> bool:
    return forecast_probability >= threshold_from_costs(false_positive_cost, false_negative_cost)


if __name__ == "__main__":
    print(round(threshold_from_costs(15.0, 85.0), 6))
    print(should_act(0.68, 15.0, 85.0))
