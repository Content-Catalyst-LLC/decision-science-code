#!/usr/bin/env python3
"""Switching cost helper."""

from __future__ import annotations


def switching_cost(investment: float, network_dependence: float, institutional_routine: float) -> float:
    return 0.36 * investment + 0.34 * network_dependence + 0.30 * institutional_routine


if __name__ == "__main__":
    print(round(switching_cost(0.55, 0.62, 0.58), 6))
