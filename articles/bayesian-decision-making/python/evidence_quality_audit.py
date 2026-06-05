#!/usr/bin/env python3
"""Evidence quality audit helper."""

from __future__ import annotations

QUALITY_SCORES = {
    "high": 1.0,
    "medium": 0.65,
    "low": 0.35,
}


def evidence_quality_score(label: str) -> float:
    return QUALITY_SCORES.get(label.lower(), 0.0)


if __name__ == "__main__":
    print(round(evidence_quality_score("medium"), 6))
