// group_error_core.c
// Compile with: cc group_error_core.c -o group_error_core

#include <stdio.h>
#include <math.h>

double collective_error(double group_estimate, double true_value) {
    return fabs(group_estimate - true_value);
}

double hidden_profile_risk(double shared_information, double unique_information) {
    return unique_information / (shared_information + unique_information);
}

int main(void) {
    printf("Collective error: %.6f\n", collective_error(0.64, 0.62));
    printf("Hidden-profile risk: %.6f\n", hidden_profile_risk(5.0, 9.0));
    return 0;
}
