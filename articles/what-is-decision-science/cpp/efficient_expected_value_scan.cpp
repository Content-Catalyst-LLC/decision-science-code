// efficient_expected_value_scan.cpp
// Compile with: g++ -std=c++17 efficient_expected_value_scan.cpp -o efficient_expected_value_scan

#include <iostream>
#include <string>
#include <vector>

double expected_value(const std::vector<double>& payoffs, const std::vector<double>& probabilities) {
    double total = 0.0;
    for (std::size_t i = 0; i < payoffs.size(); ++i) {
        total += payoffs[i] * probabilities[i];
    }
    return total;
}

int main() {
    std::vector<double> probabilities{0.40, 0.35, 0.25};

    std::vector<std::pair<std::string, std::vector<double>>> alternatives{
        {"Optimize", {120.0, 25.0, -80.0}},
        {"Hedge", {90.0, 62.0, 12.0}},
        {"Preserve Option", {66.0, 58.0, 42.0}}
    };

    for (const auto& item : alternatives) {
        std::cout << item.first << " expected value = "
                  << expected_value(item.second, probabilities) << "\n";
    }

    return 0;
}
