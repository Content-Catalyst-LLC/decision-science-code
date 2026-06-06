#!/usr/bin/env python3
"""Expected value of sample information helper."""

from __future__ import annotations


def evsi(sample_information_value: float, current_expected_value: float) -> float:
    return sample_information_value - current_expected_value


if __name__ == "__main__":
    print(round(evsi(72.5, 68.1), 6))
