// ai_governance_core.c
// Compile with: cc ai_governance_core.c -o ai_governance_core

#include <math.h>
#include <stdio.h>

double composite_ai_risk(double safety, double equity, double bias, double privacy, double opacity, double security) {
    return 0.20 * safety + 0.18 * equity + 0.16 * bias + 0.16 * privacy + 0.14 * opacity + 0.16 * security;
}

double drift_indicator(double current_metric, double baseline_metric) {
    return fabs(current_metric - baseline_metric);
}

int main(void) {
    printf("Composite AI risk: %.6f\n", composite_ai_risk(0.52, 0.48, 0.50, 0.42, 0.55, 0.46));
    printf("Drift indicator: %.6f\n", drift_indicator(0.77, 0.86));
    return 0;
}
