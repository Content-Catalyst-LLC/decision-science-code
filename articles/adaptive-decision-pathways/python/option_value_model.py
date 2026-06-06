#!/usr/bin/env python3
"""Option value helper."""

from __future__ import annotations


def option_value_next(current_option_value: float, switching_cost: float, flexibility: float) -> float:
    return max(0.0, current_option_value - 0.010 - 0.012 * switching_cost + 0.010 * flexibility)


if __name__ == "__main__":
    print(round(option_value_next(0.82, 0.34, 0.72), 6))
