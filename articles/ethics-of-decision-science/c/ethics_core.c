// Compile with: cc ethics_core.c -o ethics_core
#include <stdio.h>
double clamp(double v, double lo, double hi) { if (v < lo) return lo; if (v > hi) return hi; return v; }
double ethical_risk(double h, double o, double e, double i, double a) { return clamp(0.30*h + 0.20*o + 0.22*e + 0.18*i - 0.10*a, 0.0, 1.0); }
double legitimacy(double t, double p, double c, double a) { return 0.26*t + 0.24*p + 0.25*c + 0.25*a; }
int main(void) {
    printf("Ethical risk: %.6f\n", ethical_risk(0.64, 0.58, 0.68, 0.56, 0.46));
    printf("Legitimacy: %.6f\n", legitimacy(0.82, 0.80, 0.86, 0.90));
    return 0;
}
