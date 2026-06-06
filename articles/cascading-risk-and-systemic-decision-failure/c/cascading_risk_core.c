// cascading_risk_core.c
// Compile with: cc cascading_risk_core.c -o cascading_risk_core

#include <stdbool.h>
#include <stdio.h>

double max_double(double a, double b) {
    return a > b ? a : b;
}

double cascade_risk_score(double exposure, double dependency_centrality, double buffer_weakness, double common_mode_risk, double monitoring_quality, double response_capacity) {
    return 0.22 * exposure + 0.22 * dependency_centrality + 0.20 * buffer_weakness + 0.18 * common_mode_risk - 0.09 * monitoring_quality - 0.09 * response_capacity;
}

bool threshold_failure(double stress, double neighbor_failure_load, double buffer, double threshold) {
    double effective_stress = stress + neighbor_failure_load + max_double(0.0, 0.40 - buffer);
    return effective_stress >= threshold;
}

int main(void) {
    double score = cascade_risk_score(0.82, 0.88, 0.76, 0.79, 0.42, 0.40);
    printf("Cascade risk score: %.6f\n", score);
    printf("Threshold failure? %s\n", threshold_failure(0.52, 0.18, 0.31, 0.66) ? "true" : "false");
    return 0;
}
