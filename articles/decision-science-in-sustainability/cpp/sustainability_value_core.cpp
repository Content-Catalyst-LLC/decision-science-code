// sustainability_value_core.cpp
// Compile with: g++ -std=c++17 sustainability_value_core.cpp -o sustainability_value_core

#include <iostream>

double sustainability_value_score(double emissions_reduction, double social_equity, double cost_burden, double resilience_score, double implementation_feasibility, double threshold_protection) {
    return 0.22 * emissions_reduction + 0.20 * social_equity - 0.12 * cost_burden + 0.18 * resilience_score + 0.12 * implementation_feasibility + 0.16 * threshold_protection;
}

int main() {
    std::cout << "Sustainability value score = " << sustainability_value_score(0.61, 0.74, 0.49, 0.82, 0.66, 0.82) << "\n";
    return 0;
}
