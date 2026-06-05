// brier_score_core.c
// Compile with: cc brier_score_core.c -o brier_score_core

#include <stdio.h>
#include <math.h>

double brier_score(double probability, double outcome) {
    return pow(probability - outcome, 2.0);
}

int main(void) {
    printf("Brier score: %.6f\n", brier_score(0.72, 1.0));
    return 0;
}
