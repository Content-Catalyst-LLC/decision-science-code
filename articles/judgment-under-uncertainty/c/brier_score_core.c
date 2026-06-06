// brier_score_core.c
// Compile with: cc brier_score_core.c -o brier_score_core

#include <stdio.h>
#include <math.h>

double posterior_from_likelihoods(double prior, double likelihood_true, double likelihood_false) {
    double odds = prior / (1.0 - prior);
    double posterior_odds = odds * (likelihood_true / likelihood_false);
    return posterior_odds / (1.0 + posterior_odds);
}

double brier_score(double probability, double outcome) {
    return pow(probability - outcome, 2.0);
}

int main(void) {
    printf("Posterior: %.6f\n", posterior_from_likelihoods(0.35, 0.72, 0.28));
    printf("Brier score: %.6f\n", brier_score(0.62, 1.0));
    return 0;
}
