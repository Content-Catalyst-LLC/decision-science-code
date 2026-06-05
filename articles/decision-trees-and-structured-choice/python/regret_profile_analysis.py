#!/usr/bin/env python3
"""Regret profile helper."""

from __future__ import annotations


def regret(action_value: float, best_state_value: float) -> float:
    return best_state_value - action_value


if __name__ == "__main__":
    print(round(regret(57.8, 76.3), 4))
