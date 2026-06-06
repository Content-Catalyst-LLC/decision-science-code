#!/usr/bin/env python3
def ethical_risk(harm, opacity, exclusion, irreversibility, accountability):
    return max(0.0, min(1.0, 0.30 * harm + 0.20 * opacity + 0.22 * exclusion + 0.18 * irreversibility - 0.10 * accountability))

if __name__ == "__main__":
    print(round(ethical_risk(0.64, 0.58, 0.68, 0.56, 0.46), 6))
