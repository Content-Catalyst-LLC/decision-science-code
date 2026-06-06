// weighted_objective_core.c
// Compile with: cc weighted_objective_core.c -o weighted_objective_core

#include <stdio.h>

double weighted_score(double scores[], double weights[], int n) {
    double total = 0.0;
    for (int i = 0; i < n; i++) {
        total += scores[i] * weights[i];
    }
    return total;
}

double regret(double score, double best_score) {
    return best_score - score;
}

int main(void) {
    double scores[] = {0.90, 0.38, 0.42, 0.54, 0.48, 0.70};
    double weights[] = {0.18, 0.18, 0.20, 0.18, 0.14, 0.12};
    int n = 6;

    printf("Weighted score: %.6f\n", weighted_score(scores, weights, n));
    printf("Regret: %.6f\n", regret(0.72, 0.91));
    return 0;
}
