// weighted_quality_core.c
// Compile with: cc weighted_quality_core.c -o weighted_quality_core

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
    double weights[] = {0.11,0.10,0.12,0.13,0.11,0.10,0.11,0.11,0.11};
    double staged[] = {0.92,0.90,0.94,0.90,0.88,0.86,0.82,0.94,0.96};

    printf("Staged Learning Decision quality: %.4f\n", weighted_score(staged, weights, 9));
    return 0;
}
