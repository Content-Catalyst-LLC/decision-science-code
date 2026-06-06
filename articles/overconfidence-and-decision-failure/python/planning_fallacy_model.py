#!/usr/bin/env python3
"""Planning fallacy diagnostics."""

from __future__ import annotations


def planning_error(actual: float, estimate: float) -> float:
    if estimate == 0:
        raise ValueError("Estimate cannot be zero.")
    return (actual - estimate) / estimate


def planning_flag(error: float, threshold: float = 0.30) -> str:
    return "review" if error > threshold else "acceptable"


if __name__ == "__main__":
    error = planning_error(520, 365)
    print(round(error, 6), planning_flag(error))
