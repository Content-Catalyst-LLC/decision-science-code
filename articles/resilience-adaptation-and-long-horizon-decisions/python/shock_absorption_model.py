#!/usr/bin/env python3
"""Shock absorption helper."""

from __future__ import annotations


def absorb_shock(system_state: float, shock: float, recovery: float, adaptive_gain: float) -> float:
    return max(0.0, system_state - shock + recovery + adaptive_gain)


if __name__ == "__main__":
    print(round(absorb_shock(100.0, 8.5, 6.4, 1.2), 6))
