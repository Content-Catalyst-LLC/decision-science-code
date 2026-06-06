// sustainability_core.c
// Compile with: cc sustainability_core.c -o sustainability_core

#include <stdbool.h>
#include <stdio.h>

double sustainability_value_score(double emissions_reduction, double social_equity, double cost_burden, double resilience_score, double implementation_feasibility, double threshold_protection) {
    return 0.22 * emissions_reduction + 0.20 * social_equity - 0.12 * cost_burden + 0.18 * resilience_score + 0.12 * implementation_feasibility + 0.16 * threshold_protection;
}

bool threshold_breach(double resource_stock, double threshold) {
    return resource_stock < threshold;
}

int main(void) {
    double score = sustainability_value_score(0.61, 0.74, 0.49, 0.82, 0.66, 0.82);
    printf("Sustainability value score: %.6f\n", score);
    printf("Threshold breach? %s\n", threshold_breach(34.0, 35.0) ? "true" : "false");
    return 0;
}
