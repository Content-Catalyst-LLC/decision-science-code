// expected_utility_fast_scan.cpp
// Compile with: g++ -std=c++17 expected_utility_fast_scan.cpp -o expected_utility_fast_scan

#include <cmath>
#include <iostream>
#include <string>
#include <vector>

double utility(double value, double risk_aversion) {
    return 1.0 - std::exp(-risk_aversion * value);
}

double expected_utility(const std::vector<double>& payoffs, const std::vector<double>& probabilities, double risk_aversion) {
    double total = 0.0;
    for (std::size_t i = 0; i < payoffs.size(); ++i) {
        total += probabilities[i] * utility(payoffs[i], risk_aversion);
    }
    return total;
}

int main() {
    std::vector<double> probabilities{0.22, 0.34, 0.18, 0.16, 0.10};
    std::vector<std::pair<std::string, std::vector<double>>> strategies{
        {"Optimize", {145, 92, 30, -95, -40}},
        {"Balanced", {112, 84, 58, 12, 30}},
        {"Robust", {78, 72, 65, 48, 55}}
    };

    for (const auto& strategy : strategies) {
        std::cout << strategy.first << " EU = "
                  << expected_utility(strategy.second, probabilities, 0.018) << "\n";
    }

    return 0;
}
