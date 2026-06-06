#!/usr/bin/env python3
"""Satisficing search helper."""

from __future__ import annotations


def first_satisficing_option(values: list[float], aspiration: float) -> tuple[int, float] | None:
    for index, value in enumerate(values, start=1):
        if value >= aspiration:
            return index, value
    return None


if __name__ == "__main__":
    print(first_satisficing_option([0.58, 0.66, 0.74, 0.82], 0.75))
