#!/usr/bin/env python3
"""Automation-bias helper."""

from __future__ import annotations


def automation_bias(actual_reliance: float, justified_reliance: float) -> float:
    return actual_reliance - justified_reliance


def bias_requires_review(bias: float, threshold: float = 0.18) -> bool:
    return bias >= threshold


if __name__ == "__main__":
    bias = automation_bias(0.78, 0.56)
    print(round(bias, 6))
    print(bias_requires_review(bias))
