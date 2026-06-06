#!/usr/bin/env python3
"""Adaptive strategy simulation helper."""

from __future__ import annotations


def adaptive_growth(base_return: float, regime_shift: float, shock: float, adaptability: float, resilience: float) -> float:
    return base_return + regime_shift + shock + 0.8 * adaptability + 0.6 * resilience


if __name__ == "__main__":
    print(round(adaptive_growth(1.25, -1.0, 0.4, 1.5, 1.0), 6))
