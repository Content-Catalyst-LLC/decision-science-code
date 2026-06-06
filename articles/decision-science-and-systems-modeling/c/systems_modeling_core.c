// systems_modeling_core.c
// Compile with: cc systems_modeling_core.c -o systems_modeling_core

#include <stdio.h>

double stock_update(double stock, double inflow, double outflow) {
    return stock + inflow - outflow;
}

double feedback_update(double state, double reinforcing, double balancing, double disturbance) {
    return state + reinforcing - balancing + disturbance;
}

double systems_decision_score(double dynamic_score, double average_performance, double worst_case, double threshold_pass_rate) {
    return 0.35 * dynamic_score + 0.25 * average_performance + 0.20 * worst_case + 0.20 * threshold_pass_rate;
}

int main(void) {
    printf("Next stock: %.6f\n", stock_update(100.0, 12.0, 8.5));
    printf("Next state: %.6f\n", feedback_update(55.0, 3.85, 2.10, -0.4));
    printf("Systems decision score: %.6f\n", systems_decision_score(0.78, 0.82, 0.79, 1.0));
    return 0;
}
