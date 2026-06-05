#!/usr/bin/env python3
"""Review trigger generator."""

from __future__ import annotations


def review_trigger(realized_value: float, expected_failure_rate: float, observed_failure_rate: float) -> bool:
    return realized_value < 0 or observed_failure_rate > expected_failure_rate


if __name__ == "__main__":
    print(review_trigger(-10, 0.42, 0.50))
    print(review_trigger(72, 0.42, 0.30))
