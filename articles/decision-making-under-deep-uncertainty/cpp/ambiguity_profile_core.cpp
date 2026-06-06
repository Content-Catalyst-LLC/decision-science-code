// ambiguity_profile_core.cpp
// Compile with: g++ -std=c++17 ambiguity_profile_core.cpp -o ambiguity_profile_core

#include <iostream>
#include <vector>

double expected_value(const std::vector<double>& values, const std::vector<double>& weights) {
    double total = 0.0;
    for (size_t i = 0; i < values.size(); ++i) {
        total += values[i] * weights[i];
    }
    return total;
}

int main() {
    std::vector<double> values = {0.72, 0.80, 0.78, 0.87, 0.75, 0.77};
    std::vector<double> weights = {0.1666666667, 0.1666666667, 0.1666666667, 0.1666666667, 0.1666666667, 0.1666666667};
    std::cout << "Expected value = " << expected_value(values, weights) << "\n";
    return 0;
}
