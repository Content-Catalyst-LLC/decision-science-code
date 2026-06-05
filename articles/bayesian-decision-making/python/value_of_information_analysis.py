#!/usr/bin/env python3
"""Simple value-of-information proxy."""

from __future__ import annotations


def value_of_information(utility_with_information: float, utility_without_information: float, information_cost: float = 0.0) -> float:
    return utility_with_information - utility_without_information - information_cost


if __name__ == "__main__":
    print(round(value_of_information(44.2, 35.0, 2.0), 6))
