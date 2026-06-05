#!/usr/bin/env python3
"""Base-rate reference-class helper."""

from __future__ import annotations


def forecast_shift_from_base_rate(forecast_probability: float, base_rate: float) -> float:
    return forecast_probability - base_rate


if __name__ == "__main__":
    print(round(forecast_shift_from_base_rate(0.72, 0.58), 6))
