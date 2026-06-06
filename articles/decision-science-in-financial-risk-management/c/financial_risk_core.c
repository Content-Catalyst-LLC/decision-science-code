// financial_risk_core.c
// Compile with: cc financial_risk_core.c -o financial_risk_core

#include <stdio.h>

double expected_loss(const double losses[], const double probabilities[], int n) {
    double total = 0.0;
    for (int i = 0; i < n; i++) {
        total += losses[i] * probabilities[i];
    }
    return total;
}

double capital_next(double current_capital, double period_return_pct, double floor) {
    double next = current_capital * (1.0 + period_return_pct / 100.0);
    return next < floor ? floor : next;
}

int main(void) {
    double losses[] = {-1.2, -4.8, -3.6, -6.2};
    double probabilities[] = {0.55, 0.20, 0.15, 0.10};
    printf("Expected loss: %.6f\n", expected_loss(losses, probabilities, 4));
    printf("Capital next: %.6f\n", capital_next(100.0, -8.5, 20.0));
    return 0;
}
