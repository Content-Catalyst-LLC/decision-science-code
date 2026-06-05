#!/usr/bin/env python3
"""Regret analysis helper."""

from __future__ import annotations


def regret(action_value: float, best_value: float) -> float:
    return best_value - action_value


if __name__ == "__main__":
    print(round(regret(68.5, 79.2), 6))
