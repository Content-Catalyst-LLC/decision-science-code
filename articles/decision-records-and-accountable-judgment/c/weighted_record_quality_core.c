// weighted_record_quality_core.c
// Compile with: cc weighted_record_quality_core.c -o weighted_record_quality_core

#include <stdio.h>
#include <stddef.h>

double weighted_score(const double *scores, const double *weights, size_t n) {
    double total = 0.0;
    for (size_t i = 0; i < n; ++i) {
        total += scores[i] * weights[i];
    }
    return total;
}

double min_value(const double *scores, size_t n) {
    double min = scores[0];
    for (size_t i = 1; i < n; ++i) {
        if (scores[i] < min) {
            min = scores[i];
        }
    }
    return min;
}

int main(void) {
    double weights[] = {0.10,0.09,0.11,0.11,0.12,0.10,0.09,0.10,0.09,0.09,0.10};
    double record[] = {0.91,0.88,0.80,0.89,0.92,0.86,0.84,0.88,0.90,0.92,0.90};
    double quality = weighted_score(record, weights, 11);
    double accountable = 0.70 * quality + 0.30 * min_value(record, 11);

    printf("Accountable judgment score: %.4f\n", accountable);
    return 0;
}
