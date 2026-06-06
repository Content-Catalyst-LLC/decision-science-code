// drift_trigger_core.cpp
// Compile with: g++ -std=c++17 drift_trigger_core.cpp -o drift_trigger_core

#include <cmath>
#include <iostream>

double drift_indicator(double current_metric, double baseline_metric) {
    return std::abs(current_metric - baseline_metric);
}

int main() {
    std::cout << "Drift indicator = " << drift_indicator(0.77, 0.86) << "\n";
    return 0;
}
