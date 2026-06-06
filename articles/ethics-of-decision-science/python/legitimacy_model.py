#!/usr/bin/env python3
def legitimacy(transparency, participation, contestability, accountability):
    return 0.26 * transparency + 0.24 * participation + 0.25 * contestability + 0.25 * accountability

if __name__ == "__main__":
    print(round(legitimacy(0.82, 0.80, 0.86, 0.90), 6))
