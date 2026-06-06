#!/usr/bin/env python3
"""Equity and legitimacy review helper."""

from __future__ import annotations


def requires_equity_review(equity: float, legitimacy: float, implementation_capacity: float, threshold: float = 0.55) -> bool:
    return equity < threshold or legitimacy < threshold or implementation_capacity < threshold


if __name__ == "__main__":
    print(requires_equity_review(0.46, 0.54, 0.68))
