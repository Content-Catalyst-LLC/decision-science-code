// threshold_core.c
// Compile with: cc threshold_core.c -o threshold_core

#include <stdio.h>
#include <math.h>

double threshold_equal_utility(double a_intercept, double a_slope, double b_intercept, double b_slope) {
    double denominator = a_slope - b_slope;
    if (fabs(denominator) < 1e-12) {
        return NAN;
    }
    return (b_intercept - a_intercept) / denominator;
}

int main(void) {
    printf("Demand threshold: %.6f\n", threshold_equal_utility(70.0, 5.5, 73.0, 7.0));
    return 0;
}
