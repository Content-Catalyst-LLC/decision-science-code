// expected_value_core.cpp
// Compile with: g++ -std=c++17 expected_value_core.cpp -o expected_value_core

#include <iostream>
#include <vector>

double expected_value(const std::vector<double>& outcomes, const std::vector<double>& probabilities) {
    double total = 0.0;
    for (std::size_t i = 0; i < outcomes.size(); ++i) {
        total += outcomes[i] * probabilities[i];
    }
    return total;
}

int main() {
    std::vector<double> outcomes{180.0, 40.0};
    std::vector<double> probabilities{0.60, 0.40};
    std::cout << "Expected value = " << expected_value(outcomes, probabilities) << "\n";
    return 0;
}
