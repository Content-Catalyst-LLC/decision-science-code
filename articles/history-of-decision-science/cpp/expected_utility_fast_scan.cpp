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
    std::vector<double> probabilities{0.42, 0.28, 0.18, 0.12};
    std::vector<std::pair<std::string, std::vector<double>>> strategies{
        {"Aggressive", {128, 50, -90, -20}},
        {"Balanced", {92, 68, 18, 42}},
        {"Defensive", {62, 58, 44, 54}},
        {"Adaptive", {88, 70, 36, 72}}
    };

    for (const auto& strategy : strategies) {
        std::cout << strategy.first << " EU = "
                  << expected_utility(strategy.second, probabilities, 0.016) << "\n";
    }

    return 0;
}
