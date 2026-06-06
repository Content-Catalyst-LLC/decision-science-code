// lock_in_risk_core.cpp
// Compile with: g++ -std=c++17 lock_in_risk_core.cpp -o lock_in_risk_core

#include <iostream>

double lock_in_risk(double switching_cost, double institutional_routine, double network_dependence, double option_value) {
    return 0.42 * switching_cost + 0.28 * institutional_routine + 0.20 * network_dependence - 0.10 * option_value;
}

int main() {
    std::cout << "Lock-in risk = " << lock_in_risk(0.58, 0.62, 0.55, 0.40) << "\n";
    return 0;
}
