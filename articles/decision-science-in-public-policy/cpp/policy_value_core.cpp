// policy_value_core.cpp
// Compile with: g++ -std=c++17 policy_value_core.cpp -o policy_value_core

#include <iostream>

double policy_value_score(double efficiency, double equity, double resilience, double feasibility, double legitimacy, double implementation_capacity) {
    return 0.18 * efficiency + 0.22 * equity + 0.18 * resilience + 0.14 * feasibility + 0.14 * legitimacy + 0.14 * implementation_capacity;
}

int main() {
    std::cout << "Policy value score = " << policy_value_score(0.72, 0.84, 0.70, 0.76, 0.80, 0.86) << "\n";
    return 0;
}
