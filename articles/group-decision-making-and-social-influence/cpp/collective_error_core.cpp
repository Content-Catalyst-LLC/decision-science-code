// collective_error_core.cpp
// Compile with: g++ -std=c++17 collective_error_core.cpp -o collective_error_core

#include <cmath>
#include <iostream>

double collective_error(double group_estimate, double true_value) {
    return std::abs(group_estimate - true_value);
}

int main() {
    std::cout << "Collective error = " << collective_error(0.64, 0.62) << "\n";
    return 0;
}
