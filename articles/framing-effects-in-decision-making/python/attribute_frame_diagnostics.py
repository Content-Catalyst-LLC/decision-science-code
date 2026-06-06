#!/usr/bin/env python3
"""Attribute-frame equivalence helper."""

from __future__ import annotations


def attribute_equivalence_gap(positive_value: float, negative_value: float) -> float:
    return abs((1.0 - positive_value) - negative_value)


if __name__ == "__main__":
    print(round(attribute_equivalence_gap(0.90, 0.10), 6))
