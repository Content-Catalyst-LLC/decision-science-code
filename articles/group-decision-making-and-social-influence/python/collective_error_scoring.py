#!/usr/bin/env python3
"""Collective error scoring helper."""

from __future__ import annotations


def collective_error(group_estimate: float, true_value: float) -> float:
    return abs(group_estimate - true_value)


if __name__ == "__main__":
    print(round(collective_error(0.64, 0.62), 6))
