#!/usr/bin/env python3
"""Reference-point sensitivity helper."""

from __future__ import annotations


def reference_shift_value(value_under_r1: float, value_under_r2: float) -> float:
    return value_under_r1 - value_under_r2


if __name__ == "__main__":
    print(round(reference_shift_value(120.5, 92.25), 6))
