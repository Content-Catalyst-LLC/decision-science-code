// forecast_error_core.c
// Compile with: cc forecast_error_core.c -o forecast_error_core

#include <stdio.h>
#include <math.h>

double brier_score(double probability, double outcome) {
    return pow(probability - outcome, 2.0);
}

double threshold_from_costs(double false_positive_cost, double false_negative_cost) {
    return false_positive_cost / (false_positive_cost + false_negative_cost);
}

int main(void) {
    printf("Brier score: %.6f\n", brier_score(0.62, 1.0));
    printf("Decision threshold: %.6f\n", threshold_from_costs(15.0, 85.0));
    return 0;
}
