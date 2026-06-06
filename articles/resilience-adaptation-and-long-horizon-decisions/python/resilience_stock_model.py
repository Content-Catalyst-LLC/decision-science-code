#!/usr/bin/env python3
"""Resilience stock helper."""

from __future__ import annotations


def resilience_update(current: float, recovery: float, investment: float, degradation: float, shock: float) -> float:
    return max(0.0, current + recovery + investment - degradation - shock)


if __name__ == "__main__":
    print(round(resilience_update(35.0, 3.0, 2.0, 1.0, 1.6), 6))
