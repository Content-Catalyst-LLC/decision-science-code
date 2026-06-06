// governance_core.c
// Compile with: cc governance_core.c -o governance_core

#include <stdio.h>

double accountability_score(double decision_rights, double traceability, double review, double ownership, double monitoring, double corrective) {
    return 0.18 * decision_rights + 0.17 * traceability + 0.18 * review + 0.17 * ownership + 0.15 * monitoring + 0.15 * corrective;
}

double responsibility_gap(double influence, double accountability) {
    double gap = influence - accountability;
    return gap > 0.0 ? gap : 0.0;
}

int main(void) {
    printf("Accountability score: %.6f\n", accountability_score(0.82, 0.86, 0.88, 0.84, 0.90, 0.92));
    printf("Responsibility gap: %.6f\n", responsibility_gap(0.62, 0.34));
    return 0;
}
