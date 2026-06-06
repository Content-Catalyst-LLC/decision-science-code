// scenario_choice_core.c
// Compile with: cc scenario_choice_core.c -o scenario_choice_core

#include <stdio.h>

double expected_value(const double values[], const double probabilities[], int n) {
    double total = 0.0;
    for (int i = 0; i < n; i++) {
        total += values[i] * probabilities[i];
    }
    return total;
}

double worst_case(const double values[], int n) {
    double worst = values[0];
    for (int i = 1; i < n; i++) {
        if (values[i] < worst) {
            worst = values[i];
        }
    }
    return worst;
}

double threshold_pass_rate(const double values[], int n, double threshold) {
    int count = 0;
    for (int i = 0; i < n; i++) {
        if (values[i] >= threshold) {
            count++;
        }
    }
    return (double) count / (double) n;
}

int main(void) {
    double values[] = {0.78, 0.76, 0.82, 0.80, 0.81};
    double probabilities[] = {0.22, 0.24, 0.20, 0.18, 0.16};
    int n = 5;

    printf("Expected value: %.6f\n", expected_value(values, probabilities, n));
    printf("Worst case: %.6f\n", worst_case(values, n));
    printf("Threshold pass rate: %.6f\n", threshold_pass_rate(values, n, 0.70));
    return 0;
}
