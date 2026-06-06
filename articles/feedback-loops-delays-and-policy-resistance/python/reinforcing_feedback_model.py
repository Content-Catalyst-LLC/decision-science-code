#!/usr/bin/env python3
"""Reinforcing feedback helper."""

from __future__ import annotations


def reinforcing_effect(state: float, rate: float) -> float:
    return state * rate


if __name__ == "__main__":
    print(round(reinforcing_effect(50.0, 0.08), 6))
