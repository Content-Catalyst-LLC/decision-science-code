#!/usr/bin/env python3
"""Hidden-profile risk diagnostics."""

from __future__ import annotations


def hidden_profile_risk(shared_information: int, unique_information: int) -> float:
    total = shared_information + unique_information
    if total <= 0:
        raise ValueError("Information total must be positive.")
    return unique_information / total


if __name__ == "__main__":
    print(round(hidden_profile_risk(5, 9), 6))
