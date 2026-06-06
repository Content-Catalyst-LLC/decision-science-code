#include <stdio.h>
double expected_value(double values[], double weights[], int n) { double total = 0.0; for (int i = 0; i < n; i++) total += values[i] * weights[i]; return total; }
double worst_case(double values[], int n) { double worst = values[0]; for (int i = 1; i < n; i++) if (values[i] < worst) worst = values[i]; return worst; }
double pass_rate(double values[], int n, double threshold) { int passed = 0; for (int i = 0; i < n; i++) if (values[i] >= threshold) passed++; return (double)passed / (double)n; }
int main(void) { double values[] = {0.73, 0.77, 0.79, 0.81, 0.76, 0.86}; double weights[] = {0.18, 0.17, 0.18, 0.16, 0.15, 0.16}; int n = 6; printf("Expected value: %.6f\n", expected_value(values, weights, n)); printf("Worst case: %.6f\n", worst_case(values, n)); printf("Pass rate: %.6f\n", pass_rate(values, n, 0.70)); return 0; }
