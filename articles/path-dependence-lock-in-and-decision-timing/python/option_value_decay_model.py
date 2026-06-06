#!/usr/bin/env python3
"""Option value decay helper."""

from __future__ import annotations


def option_value_next(current_option_value: float, option_decay: float, institutional_routine: float) -> float:
    return max(0.0, current_option_value - option_decay - 0.006 * institutional_routine)


if __name__ == "__main__":
    print(round(option_value_next(0.84, 0.011, 0.35), 6))
