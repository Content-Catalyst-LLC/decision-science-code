// evpi_core.cpp
// Compile with: g++ -std=c++17 evpi_core.cpp -o evpi_core

#include <iostream>
#include <vector>

double expected_value(const std::vector<double>& values, const std::vector<double>& probabilities) {
    double total = 0.0;
    for (size_t i = 0; i < values.size(); ++i) {
        total += values[i] * probabilities[i];
    }
    return total;
}

double evpi(double perfect_information_value, double current_expected_value) {
    return perfect_information_value - current_expected_value;
}

int main() {
    std::vector<double> values = {82.0, 28.0, 40.0, 76.0};
    std::vector<double> probabilities = {0.35, 0.25, 0.20, 0.20};
    std::cout << "Expected value = " << expected_value(values, probabilities) << "\n";
    std::cout << "EVPI = " << evpi(76.4, 68.1) << "\n";
    return 0;
}
