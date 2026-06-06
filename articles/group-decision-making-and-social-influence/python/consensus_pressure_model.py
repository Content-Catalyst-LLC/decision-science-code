#!/usr/bin/env python3
"""Consensus pressure helper."""

from __future__ import annotations


def influenced_estimate(independent_estimate: float, group_mean: float, consensus_pressure: float) -> float:
    return (1.0 - consensus_pressure) * independent_estimate + consensus_pressure * group_mean


if __name__ == "__main__":
    print(round(influenced_estimate(0.70, 0.60, 0.45), 6))
