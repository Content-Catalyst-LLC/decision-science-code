// future_decision_core.c
// Compile with: cc future_decision_core.c -o future_decision_core

#include <stdio.h>

double clamp(double value, double low, double high) {
    if (value < low) return low;
    if (value > high) return high;
    return value;
}

double future_maturity(double ai, double governance, double uncertainty, double legitimacy, double reproducibility, double systems, double ethics, double adaptive, double failure) {
    return clamp(0.12 * ai + 0.14 * governance + 0.14 * uncertainty + 0.12 * legitimacy + 0.12 * reproducibility + 0.12 * systems + 0.14 * ethics + 0.14 * adaptive - 0.14 * failure, 0.0, 1.0);
}

int main(void) {
    printf("Future maturity: %.6f\n", future_maturity(0.86, 0.90, 0.88, 0.84, 0.88, 0.86, 0.90, 0.88, 0.24));
    return 0;
}
