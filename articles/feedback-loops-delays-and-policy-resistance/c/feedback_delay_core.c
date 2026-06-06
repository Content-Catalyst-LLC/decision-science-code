// feedback_delay_core.c
// Compile with: cc feedback_delay_core.c -o feedback_delay_core

#include <stdio.h>

double feedback_update(double state, double reinforcing, double balancing, double resistance, double disturbance) {
    return state + reinforcing - balancing + resistance + disturbance;
}

double net_policy_effect(double policy_delta, double intended_strength, double resistance_strength, double resistance_response) {
    return intended_strength * policy_delta - resistance_strength * resistance_response;
}

double feedback_adjusted_score(double dynamic_score, double average_performance, double worst_case, double threshold_pass_rate) {
    return 0.35 * dynamic_score + 0.25 * average_performance + 0.20 * worst_case + 0.20 * threshold_pass_rate;
}

int main(void) {
    printf("Next state: %.6f\n", feedback_update(50.0, 4.0, 1.12, 0.4, -0.3));
    printf("Net policy effect: %.6f\n", net_policy_effect(10.0, 0.8, 0.4, 6.0));
    printf("Feedback-adjusted score: %.6f\n", feedback_adjusted_score(0.42, 0.79, 0.76, 1.0));
    return 0;
}
