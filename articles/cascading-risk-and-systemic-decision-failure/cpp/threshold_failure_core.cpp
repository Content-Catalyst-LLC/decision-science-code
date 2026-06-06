// threshold_failure_core.cpp
// Compile with: g++ -std=c++17 threshold_failure_core.cpp -o threshold_failure_core

#include <algorithm>
#include <iostream>

bool threshold_failure(double stress, double neighbor_failure_load, double buffer, double threshold) {
    double effective_stress = stress + neighbor_failure_load + std::max(0.0, 0.40 - buffer);
    return effective_stress >= threshold;
}

int main() {
    std::cout << "Threshold failure? " << threshold_failure(0.52, 0.18, 0.31, 0.66) << "\n";
    return 0;
}
