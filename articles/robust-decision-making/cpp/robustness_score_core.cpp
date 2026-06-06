#include <iostream>
double robustness_score(double worst_case, double pass_rate, double max_regret, double expected_value, double performance_range) { return 0.30 * worst_case + 0.25 * pass_rate + 0.20 * (1.0 - max_regret) + 0.15 * expected_value + 0.10 * (1.0 - performance_range); }
int main() { std::cout << "Robustness score = " << robustness_score(0.73, 1.0, 0.10, 0.79, 0.13) << "\n"; return 0; }
