#!/usr/bin/env python3
"""Stock-and-flow helper."""

from __future__ import annotations


def stock_update(stock: float, inflow: float, outflow: float) -> float:
    return stock + inflow - outflow


if __name__ == "__main__":
    print(round(stock_update(100.0, 12.0, 8.5), 6))
