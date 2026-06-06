// healthcare_core.c
// Compile with: cc healthcare_core.c -o healthcare_core

#include <stdio.h>

double treatment_value_score(double expected_benefit, double adverse_event_risk, double cost_burden, double patient_preference_fit, double equity_score, double implementation_feasibility) {
    return 0.30 * expected_benefit - 0.18 * adverse_event_risk - 0.14 * cost_burden + 0.18 * patient_preference_fit + 0.10 * equity_score + 0.10 * implementation_feasibility;
}

double queue_next(double current_queue, double arrivals, double discharges) {
    double next = current_queue + arrivals - discharges;
    return next < 0.0 ? 0.0 : next;
}

int main(void) {
    double score = treatment_value_score(0.72, 0.12, 0.54, 0.88, 0.76, 0.70);
    printf("Treatment value score: %.6f\n", score);
    printf("Queue next: %.6f\n", queue_next(18.0, 24.0, 22.0));
    return 0;
}
