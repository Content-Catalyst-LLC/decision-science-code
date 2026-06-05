// sensitivity_core.cpp
// Compile with: g++ -std=c++17 sensitivity_core.cpp -o sensitivity_core

#include <cmath>
#include <iostream>

double strategy_score(
    double base,
    double demand_sensitivity,
    double cost_sensitivity,
    double disruption_sensitivity,
    double resilience_buffer,
    double adaptation_capacity,
    double demand,
    double cost,
    double disruption
) {
    return base
        + demand_sensitivity * demand
        - cost_sensitivity * cost
        - disruption_sensitivity * disruption
        + resilience_buffer * std::max(0.0, disruption)
        + adaptation_capacity * std::abs(demand);
}

int main() {
    std::cout << "Balanced score = "
              << strategy_score(75.0, 8.0, 10.0, 11.0, 9.0, 7.0, 0.5, 0.3, 0.2)
              << "\n";
    return 0;
}
