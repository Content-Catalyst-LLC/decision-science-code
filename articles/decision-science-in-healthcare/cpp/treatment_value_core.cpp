// treatment_value_core.cpp
// Compile with: g++ -std=c++17 treatment_value_core.cpp -o treatment_value_core

#include <iostream>

double treatment_value_score(double expected_benefit, double adverse_event_risk, double cost_burden, double patient_preference_fit, double equity_score, double implementation_feasibility) {
    return 0.30 * expected_benefit - 0.18 * adverse_event_risk - 0.14 * cost_burden + 0.18 * patient_preference_fit + 0.10 * equity_score + 0.10 * implementation_feasibility;
}

int main() {
    std::cout << "Treatment value score = " << treatment_value_score(0.72, 0.12, 0.54, 0.88, 0.76, 0.70) << "\n";
    return 0;
}
