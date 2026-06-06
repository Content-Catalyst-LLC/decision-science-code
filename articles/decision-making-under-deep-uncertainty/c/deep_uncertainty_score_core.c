// deep_uncertainty_score_core.c
// Compile with: cc deep_uncertainty_score_core.c -o deep_uncertainty_score_core

#include <stdio.h>

double expected_value(double values[], double weights[], int n) {
    double total = 0.0;
    for (int i = 0; i < n; i++) {
        total += values[i] * weights[i];
    }
    return total;
}

double worst_case(double values[], int n) {
    double worst = values[0];
    for (int i = 1; i < n; i++) {
        if (values[i] < worst) {
            worst = values[i];
        }
    }
    return worst;
}

double pass_rate(double values[], int n, double threshold) {
    int passed = 0;
    for (int i = 0; i < n; i++) {
        if (values[i] >= threshold) {
            passed++;
        }
    }
    return (double)passed / (double)n;
}

int main(void) {
    double values[] = {0.72, 0.80, 0.78, 0.87, 0.75, 0.77};
    double weights[] = {0.1666666667, 0.1666666667, 0.1666666667, 0.1666666667, 0.1666666667, 0.1666666667};
    int n = 6;

    printf("Expected value: %.6f\n", expected_value(values, weights, n));
    printf("Worst case: %.6f\n", worst_case(values, n));
    printf("Pass rate: %.6f\n", pass_rate(values, n, 0.70));
    return 0;
}
