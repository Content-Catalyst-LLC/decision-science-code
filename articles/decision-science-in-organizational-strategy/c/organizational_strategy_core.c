// organizational_strategy_core.c
// Compile with: cc organizational_strategy_core.c -o organizational_strategy_core

#include <stdio.h>

double expected_value(const double values[], const double probabilities[], int n) {
    double total = 0.0;
    for (int i = 0; i < n; i++) {
        total += values[i] * probabilities[i];
    }
    return total;
}

double robust_strategy_score(double expected_value, double downside_robustness, double adaptability, double reversibility) {
    return 0.36 * expected_value / 100.0 + 0.30 * downside_robustness / 100.0 + 0.20 * adaptability + 0.14 * reversibility;
}

int main(void) {
    double values[] = {68.0, 82.0, 89.0, 66.0};
    double probabilities[] = {0.25, 0.35, 0.20, 0.20};
    double ev = expected_value(values, probabilities, 4);
    printf("Expected strategic value: %.6f\n", ev);
    printf("Robust strategy score: %.6f\n", robust_strategy_score(ev, 66.0, 0.84, 0.82));
    return 0;
}
