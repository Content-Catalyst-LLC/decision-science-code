// historical_expected_value_core.c
// Compile with: cc historical_expected_value_core.c -o historical_expected_value_core

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
    double p[] = {0.42, 0.28, 0.18, 0.12};
    double aggressive[] = {128.0, 50.0, -90.0, -20.0};
    double balanced[] = {92.0, 68.0, 18.0, 42.0};
    double defensive[] = {62.0, 58.0, 44.0, 54.0};
    double adaptive[] = {88.0, 70.0, 36.0, 72.0};

    printf("Aggressive EV: %.3f\n", expected_value(aggressive, p, 4));
    printf("Balanced EV: %.3f\n", expected_value(balanced, p, 4));
    printf("Defensive EV: %.3f\n", expected_value(defensive, p, 4));
    printf("Adaptive EV: %.3f\n", expected_value(adaptive, p, 4));

    return 0;
}
