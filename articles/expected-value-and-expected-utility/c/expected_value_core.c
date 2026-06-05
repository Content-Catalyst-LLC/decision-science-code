// expected_value_core.c
// Compile with: cc expected_value_core.c -o expected_value_core

#include <stdio.h>
#include <stddef.h>

double expected_value(const double *outcomes, const double *probabilities, size_t n) {
    double total = 0.0;
    for (size_t i = 0; i < n; ++i) {
        total += outcomes[i] * probabilities[i];
    }
    return total;
}

int main(void) {
    double outcomes[] = {180.0, 40.0};
    double probabilities[] = {0.60, 0.40};
    printf("Expected value: %.4f\n", expected_value(outcomes, probabilities, 2));
    return 0;
}
