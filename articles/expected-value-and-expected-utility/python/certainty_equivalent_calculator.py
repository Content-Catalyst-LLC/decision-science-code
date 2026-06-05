#!/usr/bin/env python3
"""Certainty equivalent calculator for CRRA utility."""

from __future__ import annotations

import math


def inverse_crra(u: float, rho: float, offset: float = 151.0) -> float:
    if abs(rho - 1.0) < 1e-9:
        return math.exp(u) - offset
    return ((u * (1.0 - rho) + 1.0) ** (1.0 / (1.0 - rho))) - offset


if __name__ == "__main__":
    print(round(inverse_crra(5.2, 1.0), 4))
