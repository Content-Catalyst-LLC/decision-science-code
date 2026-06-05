#!/usr/bin/env python3
"""Value-of-information helper."""

from __future__ import annotations


def net_value_of_information(ev_with_information: float, ev_without_information: float, information_cost: float) -> float:
    return ev_with_information - ev_without_information - information_cost


if __name__ == "__main__":
    print(round(net_value_of_information(76.3, 57.8, 12.0), 4))
