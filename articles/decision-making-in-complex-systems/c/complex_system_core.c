// complex_system_core.c
// Compile with: cc complex_system_core.c -o complex_system_core

#include <stdio.h>

double complex_system_score(double adaptability, double robustness, double feedback, double interdependence, double burden, double legitimacy, double threshold_resilience) {
    return 0.18 * adaptability + 0.18 * robustness + 0.16 * feedback + 0.16 * interdependence - 0.10 * burden + 0.12 * legitimacy + 0.20 * threshold_resilience;
}

double feedback_update(double state, double reinforcing, double balancing, double disturbance) {
    return state + reinforcing - balancing + disturbance;
}

int main(void) {
    printf("Complex-system score: %.6f\n", complex_system_score(0.81, 0.86, 0.82, 0.83, 0.44, 0.78, 0.86));
    printf("Next state: %.6f\n", feedback_update(52.0, 3.0, 1.4, -0.2));
    return 0;
}
