// utility_and_regret_core.c
// Compile with: cc utility_and_regret_core.c -lm -o utility_and_regret_core

#include <math.h>
#include <stdio.h>
#include <stddef.h>

double utility(double value, double risk_aversion) {
    return 1.0 - exp(-risk_aversion * value);
}

double expected_utility(const double *payoffs, const double *probabilities, size_t n, double risk_aversion) {
    double total = 0.0;
    for (size_t i = 0; i < n; ++i) {
        total += probabilities[i] * utility(payoffs[i], risk_aversion);
    }
    return total;
}

int main(void) {
    double p[] = {0.22, 0.34, 0.18, 0.16, 0.10};
    double optimize[] = {145.0, 92.0, 30.0, -95.0, -40.0};
    double robust[] = {78.0, 72.0, 65.0, 48.0, 55.0};

    printf("Optimize EU: %.6f\n", expected_utility(optimize, p, 5, 0.018));
    printf("Robust EU: %.6f\n", expected_utility(robust, p, 5, 0.018));

    return 0;
}
