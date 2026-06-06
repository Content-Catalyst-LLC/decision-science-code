// decision_quality_core.c
// Compile with: cc decision_quality_core.c -o decision_quality_core

#include <stdio.h>
#include <math.h>

double weighted_score(double scores[], double weights[], int n) {
    double total = 0.0;
    for (int i = 0; i < n; i++) {
        total += scores[i] * weights[i];
    }
    return total;
}

double cosine_similarity(double a[], double b[], int n) {
    double dot = 0.0;
    double norm_a = 0.0;
    double norm_b = 0.0;

    for (int i = 0; i < n; i++) {
        dot += a[i] * b[i];
        norm_a += a[i] * a[i];
        norm_b += b[i] * b[i];
    }

    return dot / (sqrt(norm_a) * sqrt(norm_b));
}

int main(void) {
    double scores[] = {0.86, 0.88, 0.82, 0.86, 0.89, 0.77};
    double weights[] = {0.16, 0.15, 0.17, 0.18, 0.18, 0.16};
    double a[] = {0.68, 0.88, 0.82, 0.93, 0.86};
    double s[] = {0.20, 0.25, 0.18, 0.22, 0.15};

    printf("Decision quality score: %.6f\n", weighted_score(scores, weights, 6));
    printf("Cosine alignment: %.6f\n", cosine_similarity(a, s, 5));
    return 0;
}
