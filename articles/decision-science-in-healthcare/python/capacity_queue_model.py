#!/usr/bin/env python3
"""Capacity and queue helper."""

from __future__ import annotations


def queue_next(current_queue: float, arrivals: float, discharges: float) -> float:
    return max(0.0, current_queue + arrivals - discharges)


def queue_pressure(queue: float, reference_capacity: float = 60.0) -> float:
    return min(1.0, queue / reference_capacity)


if __name__ == "__main__":
    next_queue = queue_next(18.0, 24.0, 22.0)
    print(round(next_queue, 6))
    print(round(queue_pressure(next_queue), 6))
