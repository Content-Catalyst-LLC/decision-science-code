// bias_noise_core.c
// Compile with: cc bias_noise_core.c -o bias_noise_core

#include <stdio.h>
#include <math.h>

double bias(double values[], int n) {
    double total = 0.0;
    for (int i = 0; i < n; i++) {
        total += values[i];
    }
    return total / n;
}

double mse(double values[], int n) {
    double total = 0.0;
    for (int i = 0; i < n; i++) {
        total += values[i] * values[i];
    }
    return total / n;
}

double brier_score(double probability, double outcome) {
    return pow(probability - outcome, 2.0);
}

int main(void) {
    double errors[] = {0.12, 0.04, -0.03, 0.08};
    int n = 4;

    printf("Bias: %.6f\n", bias(errors, n));
    printf("MSE: %.6f\n", mse(errors, n));
    printf("Brier score: %.6f\n", brier_score(0.69, 0.0));

    return 0;
}
