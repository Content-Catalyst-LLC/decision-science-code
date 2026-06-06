// public_policy_core.c
// Compile with: cc public_policy_core.c -o public_policy_core

#include <stdbool.h>
#include <stdio.h>

double policy_value_score(double efficiency, double equity, double resilience, double feasibility, double legitimacy, double implementation_capacity) {
    return 0.18 * efficiency + 0.22 * equity + 0.18 * resilience + 0.14 * feasibility + 0.14 * legitimacy + 0.14 * implementation_capacity;
}

bool requires_review(double equity, double legitimacy, double implementation_capacity) {
    return equity < 0.55 || legitimacy < 0.55 || implementation_capacity < 0.55;
}

int main(void) {
    double score = policy_value_score(0.72, 0.84, 0.70, 0.76, 0.80, 0.86);
    printf("Policy value score: %.6f\n", score);
    printf("Requires review? %s\n", requires_review(0.46, 0.54, 0.68) ? "true" : "false");
    return 0;
}
