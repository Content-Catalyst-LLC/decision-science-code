#!/usr/bin/env python3
"""Log-loss calculator."""

from __future__ import annotations

import math


def clamp(value: float, low: float = 0.01, high: float = 0.99) -> float:
    return max(low, min(high, value))


def log_loss(probability: float, outcome: int) -> float:
    probability = clamp(probability)
    return -(outcome * math.log(probability) + (1 - outcome) * math.log(1 - probability))


if __name__ == "__main__":
    print(round(log_loss(0.72, 1), 6))
    print(round(log_loss(0.84, 0), 6))
