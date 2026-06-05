#!/usr/bin/env python3
"""Decision record completeness score."""

from __future__ import annotations


def completeness_score(fields_present: dict[str, bool]) -> float:
    if not fields_present:
        return 0.0
    return sum(1 for value in fields_present.values() if value) / len(fields_present)


if __name__ == "__main__":
    fields = {
        "frame": True,
        "alternatives": True,
        "evidence": True,
        "assumptions": True,
        "uncertainty": True,
        "tradeoffs": True,
        "dissent": False,
        "monitoring": True,
        "review_triggers": False,
    }
    print(round(completeness_score(fields), 4))
