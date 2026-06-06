#!/usr/bin/env python3
"""Adaptive performance helper."""

from __future__ import annotations


def expected_growth(base: float, quality: float, alignment: float, readiness: float) -> float:
    return base + 0.40 * quality + 0.35 * alignment + 0.25 * readiness


if __name__ == "__main__":
    print(round(expected_growth(0.5, 0.82, 0.88, 0.77), 6))
