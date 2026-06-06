// value_of_information_core.c
// Compile with: cc value_of_information_core.c -o value_of_information_core

#include <stdio.h>

double expected_value(double values[], double probabilities[], int n) {
    double total = 0.0;
    for (int i = 0; i < n; i++) {
        total += values[i] * probabilities[i];
    }
    return total;
}

double evpi(double perfect_information_value, double current_expected_value) {
    return perfect_information_value - current_expected_value;
}

double net_value_waiting(double evsi, double information_cost, double delay_cost) {
    return evsi - information_cost - delay_cost;
}

int main(void) {
    double values[] = {82.0, 28.0, 40.0, 76.0};
    double probabilities[] = {0.35, 0.25, 0.20, 0.20};
    int n = 4;

    printf("Expected value: %.6f\n", expected_value(values, probabilities, n));
    printf("EVPI: %.6f\n", evpi(76.4, 68.1));
    printf("Net value waiting: %.6f\n", net_value_waiting(4.4, 2.0, 1.3));
    return 0;
}
