#include <stdio.h>

double crisis_risk(double likelihood, double severity, double exposure, double vulnerability, double criticality) {
    return likelihood * severity * exposure * vulnerability * criticality;
}

int main(void) {
    printf("Crisis risk: %.6f\n", crisis_risk(0.72, 0.86, 0.68, 0.62, 0.90));
    return 0;
}
