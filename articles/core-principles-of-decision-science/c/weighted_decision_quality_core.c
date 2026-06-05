// weighted_decision_quality_core.c
// Compile with: cc weighted_decision_quality_core.c -o weighted_decision_quality_core

#include <stdio.h>
#include <stddef.h>

double weighted_score(const double *scores, const double *weights, size_t n) {
    double total = 0.0;
    for (size_t i = 0; i < n; ++i) {
        total += scores[i] * weights[i];
    }
    return total;
}

int main(void) {
    double weights[] = {0.12, 0.14, 0.12, 0.10, 0.11, 0.14, 0.12, 0.08, 0.07};
    double adaptive[] = {0.88, 0.87, 0.85, 0.84, 0.86, 0.86, 0.93, 0.84, 0.88};

    printf("Adaptive Learning Strategy score: %.4f\n", weighted_score(adaptive, weights, 9));
    return 0;
}
