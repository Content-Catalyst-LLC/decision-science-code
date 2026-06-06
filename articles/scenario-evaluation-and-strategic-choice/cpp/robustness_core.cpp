// robustness_core.cpp
// Compile with: g++ -std=c++17 robustness_core.cpp -o robustness_core

#include <algorithm>
#include <iostream>
#include <numeric>
#include <vector>

double expected_value(const std::vector<double>& values, const std::vector<double>& probabilities) {
    double total = 0.0;
    for (std::size_t i = 0; i < values.size(); ++i) {
        total += values[i] * probabilities[i];
    }
    return total;
}

double worst_case(const std::vector<double>& values) {
    return *std::min_element(values.begin(), values.end());
}

int main() {
    std::vector<double> values{0.78, 0.76, 0.82, 0.80, 0.81};
    std::vector<double> probabilities{0.22, 0.24, 0.20, 0.18, 0.16};
    std::cout << "Expected value = " << expected_value(values, probabilities) << "\n";
    std::cout << "Worst case = " << worst_case(values) << "\n";
    return 0;
}
