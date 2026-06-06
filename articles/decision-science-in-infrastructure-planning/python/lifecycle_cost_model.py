#!/usr/bin/env python3
"""Whole-life cost helper."""

from __future__ import annotations


def whole_life_cost(upfront: float, annual_operating: float, annual_maintenance: float, renewal: float, years: int, discount_rate: float) -> float:
    total = upfront
    for year in range(1, years + 1):
        total += (annual_operating + annual_maintenance) / ((1.0 + discount_rate) ** year)
    total += renewal / ((1.0 + discount_rate) ** years)
    return total


if __name__ == "__main__":
    print(round(whole_life_cost(100.0, 4.0, 2.0, 35.0, 30, 0.03), 6))
