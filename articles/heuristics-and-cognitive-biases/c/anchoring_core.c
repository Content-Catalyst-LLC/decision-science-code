// anchoring_core.c
// Compile with: cc anchoring_core.c -o anchoring_core

#include <stdio.h>
#include <math.h>

double anchored_estimate(double anchor, double evidence, double weight) {
    return weight * anchor + (1.0 - weight) * evidence;
}

double brier_score(double probability, double outcome) {
    return pow(probability - outcome, 2.0);
}

int main(void) {
    printf("Anchored estimate: %.6f\n", anchored_estimate(0.80, 0.42, 0.45));
    printf("Brier score: %.6f\n", brier_score(0.72, 1.0));
    return 0;
}
