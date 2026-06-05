#!/usr/bin/env python3
"""Decision node selector."""

from __future__ import annotations


def select_best_branch(branch_values: dict[str, float]) -> tuple[str, float]:
    if not branch_values:
        raise ValueError("No branches supplied.")
    return max(branch_values.items(), key=lambda item: item[1])


if __name__ == "__main__":
    print(select_best_branch({"Immediate": 57.8, "Staged": 64.3, "Baseline": 71.2}))
