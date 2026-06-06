#!/usr/bin/env python3
"""Regret matrix calculator helper."""

from __future__ import annotations


def regret(value: float, scenario_best: float) -> float:
    return scenario_best - value


if __name__ == "__main__":
    print(round(regret(0.72, 0.91), 6))
