// assumption_drift_core.cpp
// Compile with: g++ -std=c++17 assumption_drift_core.cpp -o assumption_drift_core

#include <algorithm>
#include <iostream>

double drift_next(double current_drift, double signal_pressure, double adaptability, double governance_support) {
    return std::max(0.0, std::min(1.0, current_drift + signal_pressure - 0.025 * adaptability - 0.015 * governance_support));
}

int main() {
    std::cout << "Assumption drift next = " << drift_next(0.20, 0.08, 0.42, 0.78) << "\n";
    return 0;
}
