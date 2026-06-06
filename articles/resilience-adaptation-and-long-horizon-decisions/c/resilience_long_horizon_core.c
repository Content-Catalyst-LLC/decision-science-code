// resilience_long_horizon_core.c
// Compile with: cc resilience_long_horizon_core.c -o resilience_long_horizon_core

#include <stdbool.h>
#include <stdio.h>

double max_double(double a, double b) {
    return a > b ? a : b;
}

double resilience_update(double current, double recovery, double investment, double degradation, double shock) {
    return max_double(0.0, current + recovery + investment - degradation - shock);
}

double resilient_decision_score(double long_horizon_score, double average_performance, double worst_case, double pass_rate, double performance_range) {
    return 0.30 * long_horizon_score + 0.24 * average_performance + 0.22 * worst_case + 0.18 * pass_rate - 0.06 * performance_range;
}

bool should_revise(double system_state, double resilience_capacity, double stress_threshold, double resilience_threshold) {
    return system_state >= stress_threshold || resilience_capacity <= resilience_threshold;
}

int main(void) {
    printf("Next resilience stock: %.6f\n", resilience_update(35.0, 3.0, 2.0, 1.0, 1.6));
    printf("Resilient decision score: %.6f\n", resilient_decision_score(0.80, 0.79, 0.74, 1.0, 0.10));
    printf("Revise? %s\n", should_revise(72.0, 24.0, 80.0, 25.0) ? "true" : "false");
    return 0;
}
