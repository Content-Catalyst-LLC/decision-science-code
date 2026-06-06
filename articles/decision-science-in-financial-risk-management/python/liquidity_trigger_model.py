#!/usr/bin/env python3
"""Liquidity trigger helper."""

from __future__ import annotations


def liquidity_drag(base_drag: float, liquidity: float) -> float:
    return base_drag * (1.0 + max(0.0, 0.60 - liquidity))


def liquidity_trigger_hit(liquidity: float, trigger: float = 0.42) -> bool:
    return liquidity < trigger


if __name__ == "__main__":
    print(round(liquidity_drag(0.80, 0.48), 6))
    print(liquidity_trigger_hit(0.36))
