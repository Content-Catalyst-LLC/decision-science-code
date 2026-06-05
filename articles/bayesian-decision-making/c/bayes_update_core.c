// bayes_update_core.c
// Compile with: cc bayes_update_core.c -o bayes_update_core

#include <stdio.h>

double bayesian_update(double prior, double sensitivity, double false_positive_rate) {
    double numerator = sensitivity * prior;
    double denominator = numerator + false_positive_rate * (1.0 - prior);
    return numerator / denominator;
}

int main(void) {
    printf("Posterior: %.6f\n", bayesian_update(0.10, 0.86, 0.12));
    return 0;
}
