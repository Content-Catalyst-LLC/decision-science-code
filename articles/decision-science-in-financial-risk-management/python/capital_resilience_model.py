#!/usr/bin/env python3
"""Capital resilience helper."""

from __future__ import annotations


def capital_next(current_capital: float, period_return_pct: float, floor: float = 20.0) -> float:
    return max(floor, current_capital * (1.0 + period_return_pct / 100.0))


def capital_trigger_hit(capital: float, trigger: float = 72.0) -> bool:
    return capital < trigger


if __name__ == "__main__":
    c = capital_next(100.0, -8.5)
    print(round(c, 6))
    print(capital_trigger_hit(c))
