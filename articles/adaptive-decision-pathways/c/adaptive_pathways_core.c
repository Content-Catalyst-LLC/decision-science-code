// adaptive_pathways_core.c
// Compile with: cc adaptive_pathways_core.c -o adaptive_pathways_core

#include <stdbool.h>
#include <stdio.h>

double pathway_score(double initial_performance, double flexibility, double monitoring_quality, double trigger_clarity, double switching_cost, double fallback_strength) {
    return 0.20 * initial_performance + 0.18 * flexibility + 0.16 * monitoring_quality + 0.16 * trigger_clarity - 0.12 * switching_cost + 0.18 * fallback_strength;
}

bool trigger_hit(double system_stress, double option_value, double stress_trigger, double option_value_trigger) {
    return system_stress >= stress_trigger || option_value <= option_value_trigger;
}

int main(void) {
    double score = pathway_score(0.76, 0.88, 0.82, 0.80, 0.38, 0.84);
    printf("Pathway score: %.6f\n", score);
    printf("Trigger hit? %s\n", trigger_hit(0.70, 0.55, 0.68, 0.40) ? "true" : "false");
    return 0;
}
