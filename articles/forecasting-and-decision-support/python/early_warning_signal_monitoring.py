#!/usr/bin/env python3
"""Early-warning signal monitoring helper."""

from __future__ import annotations


def signal_triggered(current_value: float, threshold: float, direction: str = "above") -> bool:
    if direction == "above":
        return current_value >= threshold
    if direction == "below":
        return current_value <= threshold
    raise ValueError("Direction must be 'above' or 'below'.")


if __name__ == "__main__":
    print(signal_triggered(0.64, 0.60, "above"))
