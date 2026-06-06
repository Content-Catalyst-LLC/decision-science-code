// adaptive_revision_core.cpp
// Compile with: g++ -std=c++17 adaptive_revision_core.cpp -o adaptive_revision_core

#include <iostream>

bool should_revise(double system_state, double resilience_capacity, double stress_threshold, double resilience_threshold) {
    return system_state >= stress_threshold || resilience_capacity <= resilience_threshold;
}

int main() {
    std::cout << "Revise? " << should_revise(72.0, 24.0, 80.0, 25.0) << "\n";
    return 0;
}
