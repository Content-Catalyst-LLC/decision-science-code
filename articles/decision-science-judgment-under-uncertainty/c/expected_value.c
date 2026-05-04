#include <stdio.h>

int main(void) {
    double probabilities[] = {0.65, 0.35};
    double values[] = {72.0, 38.0};
    int n = 2;
    double expected_value = 0.0;

    for (int i = 0; i < n; i++) {
        expected_value += probabilities[i] * values[i];
    }

    printf("Expected value: %.3f\n", expected_value);

    return 0;
}
