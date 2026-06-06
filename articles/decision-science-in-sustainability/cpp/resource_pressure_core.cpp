// resource_pressure_core.cpp
// Compile with: g++ -std=c++17 resource_pressure_core.cpp -o resource_pressure_core

#include <algorithm>
#include <iostream>

double resource_next(double resource_stock, double extraction, double regeneration) {
    return std::max(0.0, resource_stock - extraction + regeneration);
}

double pressure_next(double resource_pressure, double policy_response, double governance_delay, double random_component) {
    return std::max(5.0, resource_pressure + random_component - 0.050 * policy_response + 0.030 * governance_delay);
}

int main() {
    std::cout << "Resource next = " << resource_next(100.0, 28.0, 13.2) << "\n";
    std::cout << "Pressure next = " << pressure_next(28.0, 8.0, 5.0, 0.60) << "\n";
    return 0;
}
