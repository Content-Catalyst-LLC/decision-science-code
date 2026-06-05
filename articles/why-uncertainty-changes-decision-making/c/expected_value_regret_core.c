// expected_value_regret_core.c
// Compile with: cc expected_value_regret_core.c -o expected_value_regret_core

#include <stdio.h>
#include <stddef.h>

double expected_value(const double *payoffs, const double *probabilities, size_t n) {
    double total = 0.0;
    for (size_t i = 0; i < n; ++i) {
        total += payoffs[i] * probabilities[i];
    }
    return total;
}

int main(void) {
    double p[] = {0.40, 0.24, 0.16, 0.10, 0.10};
    double expand[] = {120.0, 45.0, -95.0, -130.0, 20.0};
    double hedge[] = {92.0, 68.0, 18.0, -20.0, 55.0};
    double preserve[] = {72.0, 62.0, 42.0, 18.0, 70.0};
    double adaptive[] = {95.0, 72.0, 34.0, 10.0, 78.0};

    printf("Expand EV: %.3f\n", expected_value(expand, p, 5));
    printf("Hedge EV: %.3f\n", expected_value(hedge, p, 5));
    printf("Preserve Option EV: %.3f\n", expected_value(preserve, p, 5));
    printf("Adaptive Pathway EV: %.3f\n", expected_value(adaptive, p, 5));

    return 0;
}
