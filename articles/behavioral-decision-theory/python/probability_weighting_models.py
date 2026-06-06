#!/usr/bin/env python3
"""Probability weighting helpers."""

from __future__ import annotations


def weighted_probability(p: float, gamma: float = 0.72) -> float:
    p = max(0.000001, min(0.999999, p))
    return (p ** gamma) / ((p ** gamma + (1 - p) ** gamma) ** (1 / gamma))


if __name__ == "__main__":
    for p in [0.05, 0.10, 0.50, 0.90]:
        print(p, round(weighted_probability(p), 6))
