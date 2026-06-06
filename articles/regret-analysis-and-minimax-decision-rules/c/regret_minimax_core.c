// regret_minimax_core.c
// Compile with: cc regret_minimax_core.c -o regret_minimax_core

#include <stdio.h>

double expected_value(double values[], double weights[], int n) {
    double total = 0.0;
    for (int i = 0; i < n; i++) {
        total += values[i] * weights[i];
    }
    return total;
}

double maximin_value(double values[], int n) {
    double worst = values[0];
    for (int i = 1; i < n; i++) {
        if (values[i] < worst) {
            worst = values[i];
        }
    }
    return worst;
}

double maximum_regret(double regrets[], int n) {
    double max_value = regrets[0];
    for (int i = 1; i < n; i++) {
        if (regrets[i] > max_value) {
            max_value = regrets[i];
        }
    }
    return max_value;
}

int main(void) {
    double values[] = {0.73, 0.81, 0.79, 0.87, 0.76, 0.77};
    double weights[] = {0.18, 0.16, 0.18, 0.17, 0.15, 0.16};
    double regrets[] = {0.19, 0.00, 0.05, 0.01, 0.06, 0.06};
    int n = 6;

    printf("Expected value: %.6f\n", expected_value(values, weights, n));
    printf("Maximin value: %.6f\n", maximin_value(values, n));
    printf("Maximum regret: %.6f\n", maximum_regret(regrets, n));
    return 0;
}
