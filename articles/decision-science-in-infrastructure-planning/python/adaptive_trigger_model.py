#!/usr/bin/env python3
"""Adaptive pathway trigger helper."""

from __future__ import annotations


def trigger_reached(indicator: float, threshold: float, direction: str = "above") -> bool:
    if direction == "above":
        return indicator >= threshold
    if direction == "below":
        return indicator <= threshold
    raise ValueError("direction must be 'above' or 'below'")


def pathway_action(indicator: float, threshold: float, current_action: str, triggered_action: str, direction: str = "above") -> str:
    return triggered_action if trigger_reached(indicator, threshold, direction) else current_action


if __name__ == "__main__":
    print(trigger_reached(0.74, 0.70, "above"))
    print(pathway_action(0.74, 0.70, "monitor", "escalate_adaptation", "above"))
