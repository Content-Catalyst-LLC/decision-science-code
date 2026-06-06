// prospect_value_core.c
// Compile with: cc prospect_value_core.c -o prospect_value_core

#include <stdio.h>
#include <math.h>

double prospect_value(double x, double alpha, double beta, double loss_aversion) {
    if (x >= 0.0) {
        return pow(x, alpha);
    }
    return -loss_aversion * pow(-x, beta);
}

double weighted_probability(double p, double gamma) {
    return pow(p, gamma) / pow(pow(p, gamma) + pow(1.0 - p, gamma), 1.0 / gamma);
}

int main(void) {
    printf("Gain value: %.6f\n", prospect_value(100.0, 0.88, 0.88, 2.0));
    printf("Loss value: %.6f\n", prospect_value(-100.0, 0.88, 0.88, 2.0));
    printf("Weighted probability: %.6f\n", weighted_probability(0.10, 0.72));
    return 0;
}
