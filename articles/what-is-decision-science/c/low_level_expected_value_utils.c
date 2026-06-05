// low_level_expected_value_utils.c
// Compile with: cc low_level_expected_value_utils.c -o low_level_expected_value_utils

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
    double probabilities[] = {0.40, 0.35, 0.25};
    double optimize[] = {120.0, 25.0, -80.0};
    double hedge[] = {90.0, 62.0, 12.0};
    double preserve[] = {66.0, 58.0, 42.0};

    printf("Optimize EV: %.3f\n", expected_value(optimize, probabilities, 3));
    printf("Hedge EV: %.3f\n", expected_value(hedge, probabilities, 3));
    printf("Preserve Option EV: %.3f\n", expected_value(preserve, probabilities, 3));

    return 0;
}
