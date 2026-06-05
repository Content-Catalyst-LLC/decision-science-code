// expected_loss_core.c
// Compile with: cc expected_loss_core.c -o expected_loss_core

#include <stdio.h>
#include <stddef.h>

double expected_loss(const double *probabilities, const double *losses, size_t n) {
    double total = 0.0;
    for (size_t i = 0; i < n; ++i) {
        total += probabilities[i] * losses[i];
    }
    return total;
}

int main(void) {
    double probabilities[] = {0.08, 0.06, 0.03};
    double losses[] = {0.035, 0.040, 0.075};

    printf("Expected loss: %.6f\n", expected_loss(probabilities, losses, 3));
    return 0;
}
