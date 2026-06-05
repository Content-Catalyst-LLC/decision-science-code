#!/usr/bin/env python3
"""Decision framing diagnostics."""

from __future__ import annotations


def framing_score(has_owner: bool, has_objectives: bool, has_alternatives: bool, has_constraints: bool, has_timeline: bool) -> float:
    return sum([has_owner, has_objectives, has_alternatives, has_constraints, has_timeline]) / 5.0


if __name__ == "__main__":
    print(framing_score(True, True, True, False, True))
