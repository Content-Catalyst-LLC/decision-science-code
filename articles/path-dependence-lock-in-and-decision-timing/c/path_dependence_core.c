// path_dependence_core.c
// Compile with: cc path_dependence_core.c -o path_dependence_core

#include <stdbool.h>
#include <stdio.h>

double switching_cost(double investment, double network_dependence, double institutional_routine) {
    return 0.36 * investment + 0.34 * network_dependence + 0.30 * institutional_routine;
}

double lock_in_risk(double switching_cost, double institutional_routine, double network_dependence, double option_value) {
    return 0.42 * switching_cost + 0.28 * institutional_routine + 0.20 * network_dependence - 0.10 * option_value;
}

bool should_review(double lock_in_risk, double option_value, double lock_in_threshold, double option_threshold) {
    return lock_in_risk >= lock_in_threshold || option_value <= option_threshold;
}

int main(void) {
    double cost = switching_cost(0.55, 0.62, 0.58);
    double risk = lock_in_risk(cost, 0.62, 0.55, 0.40);

    printf("Switching cost: %.6f\n", cost);
    printf("Lock-in risk: %.6f\n", risk);
    printf("Review? %s\n", should_review(risk, 0.40, 0.72, 0.35) ? "true" : "false");

    return 0;
}
