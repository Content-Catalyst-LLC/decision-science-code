// implementation_drift_core.cpp
// Compile with: g++ -std=c++17 implementation_drift_core.cpp -o implementation_drift_core

#include <algorithm>
#include <iostream>

double drift_next(double current_drift, double feedback_quality, double implementation_capacity, double random_component) {
    return std::max(0.0, current_drift + random_component - 0.030 * feedback_quality - 0.020 * implementation_capacity);
}

int main() {
    std::cout << "Implementation drift next = " << drift_next(6.0, 12.0, 22.0, 0.40) << "\n";
    return 0;
}
