// calibration_core.c
// Compile with: cc calibration_core.c -o calibration_core

#include <stdio.h>
#include <math.h>

double brier_score(double probability, double outcome) {
    return pow(probability - outcome, 2.0);
}

double confidence_error(double confidence, double accuracy_proxy) {
    return confidence - accuracy_proxy;
}

double planning_error(double actual, double estimate) {
    return (actual - estimate) / estimate;
}

int main(void) {
    printf("Brier score: %.6f\n", brier_score(0.69, 0.0));
    printf("Confidence error: %.6f\n", confidence_error(0.88, 0.52));
    printf("Planning error: %.6f\n", planning_error(520.0, 365.0));
    return 0;
}
