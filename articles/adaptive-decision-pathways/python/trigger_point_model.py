#!/usr/bin/env python3
"""Trigger point helper."""

from __future__ import annotations


def trigger_hit(system_stress: float, option_value: float, stress_trigger: float = 0.68, option_value_trigger: float = 0.40) -> bool:
    return system_stress >= stress_trigger or option_value <= option_value_trigger


if __name__ == "__main__":
    print(trigger_hit(0.70, 0.55))
