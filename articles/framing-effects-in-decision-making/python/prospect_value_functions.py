#!/usr/bin/env python3
"""Prospect-style value function helper."""

from __future__ import annotations


def prospect_value(x: float, alpha: float = 0.88, beta: float = 0.88, loss_aversion: float = 2.0) -> float:
    if x >= 0:
        return x ** alpha
    return -loss_aversion * ((-x) ** beta)


if __name__ == "__main__":
    print(round(prospect_value(100), 6))
    print(round(prospect_value(-100), 6))
