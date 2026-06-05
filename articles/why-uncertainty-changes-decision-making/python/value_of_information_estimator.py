#!/usr/bin/env python3
"""Value-of-information estimator scaffold."""

from __future__ import annotations


def expected_value_of_information(value_with_information: float, value_without_information: float, delay_cost: float) -> float:
    return value_with_information - value_without_information - delay_cost


if __name__ == "__main__":
    print(expected_value_of_information(82.0, 68.0, 6.5))
