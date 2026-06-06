#!/usr/bin/env python3
"""Timing recommendation helper."""

from __future__ import annotations


def recommend(net_value_waiting: float, net_value_information: float, evsi: float, delay_cost: float) -> str:
    if net_value_waiting > 0:
        return "wait_for_information"
    if net_value_information > 0 and delay_cost > evsi * 0.5:
        return "learn_while_acting"
    return "act_now_or_stage"


if __name__ == "__main__":
    print(recommend(-2.0, 3.0, 6.0, 5.0))
