// infrastructure_value_core.cpp
// Compile with: g++ -std=c++17 infrastructure_value_core.cpp -o infrastructure_value_core

#include <algorithm>
#include <iostream>
#include <vector>

double expected_value(const std::vector<double>& values, const std::vector<double>& probabilities) {
    double total = 0.0;
    for (std::size_t i = 0; i < values.size(); ++i) {
        total += values[i] * probabilities[i];
    }
    return total;
}

int main() {
    std::vector<double> values{76.0, 76.0, 82.0, 70.0, 78.0};
    std::vector<double> probabilities{0.30, 0.20, 0.20, 0.15, 0.15};
    std::cout << "Expected service value = " << expected_value(values, probabilities) << "\n";
    std::cout << "Worst-case value = " << *std::min_element(values.begin(), values.end()) << "\n";
    return 0;
}
