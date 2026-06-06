// weighted_score_core.c
// Compile with: cc weighted_score_core.c -o weighted_score_core

#include <stdio.h>

double weighted_score(double scores[], double weights[], int n) {
    double total = 0.0;
    for (int i = 0; i < n; i++) {
        total += scores[i] * weights[i];
    }
    return total;
}

int main(void) {
    double scores[] = {0.8, 0.6, 0.9};
    double weights[] = {0.3, 0.3, 0.4};
    int n = 3;

    printf("Weighted score: %.6f\n", weighted_score(scores, weights, n));
    return 0;
}
