// policy_resistance_core.cpp
// Compile with: g++ -std=c++17 policy_resistance_core.cpp -o policy_resistance_core

#include <iostream>

double net_policy_effect(double policy_delta, double intended_strength, double resistance_strength, double resistance_response) {
    return intended_strength * policy_delta - resistance_strength * resistance_response;
}

int main() {
    std::cout << "Net policy effect = " << net_policy_effect(10.0, 0.8, 0.4, 6.0) << "\n";
    return 0;
}
