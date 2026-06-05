// expected_value_tree_core.c
// Compile with: cc expected_value_tree_core.c -o expected_value_tree_core

#include <stdio.h>

double expected_value(double success_payoff, double failure_payoff, double success_probability, double cost, double credit) {
    return success_payoff * success_probability + failure_payoff * (1.0 - success_probability) - cost + credit;
}

int main(void) {
    double immediate = expected_value(125.0, -35.0, 0.58, 0.0, 0.0);
    double staged = expected_value(145.0, -20.0, 0.54, 12.0, 18.0);

    printf("Immediate EV: %.4f\n", immediate);
    printf("Staged EV: %.4f\n", staged);
    printf("Net value of staging: %.4f\n", staged - immediate);
    return 0;
}
