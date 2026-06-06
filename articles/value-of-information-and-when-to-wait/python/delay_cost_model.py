#!/usr/bin/env python3
"""Delay cost helper."""

from __future__ import annotations


def net_value_waiting(evsi: float, information_cost: float, delay_cost: float) -> float:
    return evsi - information_cost - delay_cost


if __name__ == "__main__":
    print(round(net_value_waiting(4.4, 2.0, 1.3), 6))
