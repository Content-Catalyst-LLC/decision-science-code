#!/usr/bin/env python3
"""Expected value of perfect information helper."""

from __future__ import annotations


def evpi(perfect_information_value: float, current_expected_value: float) -> float:
    return perfect_information_value - current_expected_value


if __name__ == "__main__":
    print(round(evpi(76.4, 68.1), 6))
