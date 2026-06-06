// infrastructure_core.c
// Compile with: cc infrastructure_core.c -o infrastructure_core

#include <stdio.h>

double expected_value(const double values[], const double probabilities[], int n) {
    double total = 0.0;
    for (int i = 0; i < n; i++) {
        total += values[i] * probabilities[i];
    }
    return total;
}

int trigger_reached(double indicator, double threshold) {
    return indicator >= threshold;
}

int main(void) {
    double values[] = {76.0, 76.0, 82.0, 70.0, 78.0};
    double probabilities[] = {0.30, 0.20, 0.20, 0.15, 0.15};
    printf("Expected service value: %.6f\n", expected_value(values, probabilities, 5));
    printf("Adaptive trigger reached: %d\n", trigger_reached(0.74, 0.70));
    return 0;
}
