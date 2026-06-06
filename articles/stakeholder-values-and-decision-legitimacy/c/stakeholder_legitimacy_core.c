// stakeholder_legitimacy_core.c
// Compile with: cc stakeholder_legitimacy_core.c -o stakeholder_legitimacy_core

#include <stdio.h>

double weighted_score(double values[], double weights[], int n) {
    double total = 0.0;
    for (int i = 0; i < n; i++) {
        total += values[i] * weights[i];
    }
    return total;
}

double legitimacy_index(double aggregate_score, double procedural_score, double pass_rate, double min_score, double max_burden) {
    return 0.40 * aggregate_score + 0.24 * procedural_score + 0.18 * pass_rate + 0.10 * min_score - 0.08 * max_burden;
}

int main(void) {
    double values[] = {0.68, 0.80, 0.84, 0.82, 0.86, 0.90};
    double weights[] = {0.12, 0.18, 0.28, 0.14, 0.16, 0.12};
    int n = 6;

    printf("Stakeholder score: %.6f\n", weighted_score(values, weights, n));
    printf("Legitimacy index: %.6f\n", legitimacy_index(0.82, 0.89, 1.0, 0.76, 0.26));
    return 0;
}
