#!/usr/bin/env python3
"""Utility function profiles."""

from __future__ import annotations

import math


def linear_utility(x: float) -> float:
    return x


def log_utility(x: float, offset: float = 151.0) -> float:
    return math.log(x + offset)


def crra_utility(x: float, rho: float, offset: float = 151.0) -> float:
    z = x + offset
    if z <= 0:
        raise ValueError("Shifted outcome must be positive.")
    if abs(rho - 1.0) < 1e-9:
        return math.log(z)
    return (z ** (1.0 - rho) - 1.0) / (1.0 - rho)


if __name__ == "__main__":
    for rho in [0.25, 1.0, 2.25]:
        print(rho, round(crra_utility(100, rho), 6))
