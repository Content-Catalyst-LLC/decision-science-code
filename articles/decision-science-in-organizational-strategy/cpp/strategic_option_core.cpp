// strategic_option_core.cpp
// Compile with: g++ -std=c++17 strategic_option_core.cpp -o strategic_option_core

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
    std::vector<double> values{68.0, 82.0, 89.0, 66.0};
    std::vector<double> probabilities{0.25, 0.35, 0.20, 0.20};
    std::cout << "Expected strategic value = " << expected_value(values, probabilities) << "\n";
    std::cout << "Downside robustness = " << *std::min_element(values.begin(), values.end()) << "\n";
    return 0;
}
