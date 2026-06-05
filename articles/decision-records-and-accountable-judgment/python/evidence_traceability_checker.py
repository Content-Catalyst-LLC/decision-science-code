#!/usr/bin/env python3
"""Evidence traceability checker."""

from __future__ import annotations


def traceability_share(claims: list[dict[str, object]]) -> float:
    if not claims:
        return 0.0
    return sum(1 for claim in claims if bool(claim["evidence_linked"])) / len(claims)


if __name__ == "__main__":
    claims = [
        {"claim": "A", "evidence_linked": True},
        {"claim": "B", "evidence_linked": False},
        {"claim": "C", "evidence_linked": True},
    ]
    print(round(traceability_share(claims), 4))
