#!/usr/bin/env python3
"""Switching rule helper."""

from __future__ import annotations


def next_pathway(current_pathway: str, trigger_hit: bool) -> str:
    if not trigger_hit:
        return current_pathway
    if current_pathway == "baseline_path":
        return "moderate_adaptation_path"
    if current_pathway == "moderate_adaptation_path":
        return "high_resilience_path"
    return current_pathway


if __name__ == "__main__":
    print(next_pathway("baseline_path", True))
