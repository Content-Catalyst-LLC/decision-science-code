#!/usr/bin/env python3
"""Availability-bias salience model."""

from __future__ import annotations


def availability_adjusted_probability(base_probability: float, salience_multiplier: float) -> float:
    return max(0.01, min(0.99, base_probability * salience_multiplier))


if __name__ == "__main__":
    print(round(availability_adjusted_probability(0.42, 1.45), 6))
