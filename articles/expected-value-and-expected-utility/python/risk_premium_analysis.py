#!/usr/bin/env python3
"""Risk premium analysis."""

from __future__ import annotations


def risk_premium(expected_value: float, certainty_equivalent: float) -> float:
    return expected_value - certainty_equivalent


if __name__ == "__main__":
    print(round(risk_premium(116.0, 94.5), 4))
