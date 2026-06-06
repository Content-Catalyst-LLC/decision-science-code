// democratic_reasoning_core.c
// Compile with: cc democratic_reasoning_core.c -o democratic_reasoning_core

#include <stdio.h>

double clamp(double value, double low, double high) {
    if (value < low) return low;
    if (value > high) return high;
    return value;
}

double legitimacy_score(double transparency, double participation, double fairness, double evidence, double contestability, double accountability) {
    return 0.17 * transparency + 0.17 * participation + 0.18 * fairness + 0.16 * evidence + 0.16 * contestability + 0.16 * accountability;
}

double next_trust(double current, double performance, double transparency, double responsiveness, double fairness, double uncertainty, double harm) {
    return clamp(current + 0.08 * performance + 0.06 * transparency + 0.08 * responsiveness + 0.08 * fairness - 0.06 * uncertainty - 0.10 * harm, 0.0, 1.0);
}

int main(void) {
    printf("Legitimacy score: %.6f\n", legitimacy_score(0.88, 0.88, 0.88, 0.84, 0.86, 0.88));
    printf("Next trust: %.6f\n", next_trust(0.62, 0.70, 0.78, 0.74, 0.72, 0.36, 0.30));
    return 0;
}
