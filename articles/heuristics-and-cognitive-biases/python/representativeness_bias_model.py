#!/usr/bin/env python3
"""Representativeness and base-rate neglect model."""

from __future__ import annotations


def representativeness_estimate(base_rate: float, similarity_signal: float, signal_weight: float = 0.65) -> float:
    return max(0.01, min(0.99, (1 - signal_weight) * base_rate + signal_weight * similarity_signal))


if __name__ == "__main__":
    print(round(representativeness_estimate(0.30, 0.72), 6))
