#!/usr/bin/env python3
from __future__ import annotations

def trigger_reached(indicator_value: float, threshold: float, direction: str) -> bool:
    if direction == "above":
        return indicator_value > threshold
    if direction == "below":
        return indicator_value < threshold
    raise ValueError("Direction must be 'above' or 'below'.")

if __name__ == "__main__":
    print(trigger_reached(0.42, 0.35, "above"))
    print(trigger_reached(0.48, 0.50, "below"))
