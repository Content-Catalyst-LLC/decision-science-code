#!/usr/bin/env python3
"""Forecast value-of-information proxy."""

from __future__ import annotations


def expected_loss(action: bool, probability: float, false_positive_cost: float, false_negative_cost: float) -> float:
    if action:
        return (1.0 - probability) * false_positive_cost
    return probability * false_negative_cost


def forecast_value(loss_without_forecast: float, loss_with_forecast: float, forecast_cost: float) -> float:
    return loss_without_forecast - loss_with_forecast - forecast_cost


if __name__ == "__main__":
    print(round(forecast_value(25.0, 14.0, 3.5), 6))
