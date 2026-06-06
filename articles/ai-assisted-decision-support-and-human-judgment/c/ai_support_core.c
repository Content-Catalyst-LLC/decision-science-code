// ai_support_core.c
// Compile with: cc ai_support_core.c -o ai_support_core

#include <stdio.h>

double clamp(double value, double low, double high) {
    if (value < low) return low;
    if (value > high) return high;
    return value;
}

double justified_model_reliance(double evidence_quality, double calibration, double decision_risk, double uncertainty) {
    return clamp(0.35 * evidence_quality + 0.35 * calibration - 0.16 * decision_risk - 0.14 * uncertainty, 0.0, 1.0);
}

double automation_bias(double actual_reliance, double justified_reliance) {
    return actual_reliance - justified_reliance;
}

int main(void) {
    double justified = justified_model_reliance(0.82, 0.78, 0.54, 0.36);
    printf("Justified model reliance: %.6f\n", justified);
    printf("Automation bias: %.6f\n", automation_bias(0.78, justified));
    return 0;
}
