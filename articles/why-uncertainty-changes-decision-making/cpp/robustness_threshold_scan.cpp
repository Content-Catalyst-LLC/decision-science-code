// robustness_threshold_scan.cpp
// Compile with: g++ -std=c++17 robustness_threshold_scan.cpp -o robustness_threshold_scan

#include <iostream>
#include <string>
#include <vector>

double robustness(const std::vector<double>& values, double threshold) {
    int count = 0;
    for (double value : values) {
        if (value >= threshold) {
            ++count;
        }
    }
    return static_cast<double>(count) / static_cast<double>(values.size());
}

int main() {
    std::vector<std::pair<std::string, std::vector<double>>> strategies{
        {"Expand", {120, 45, -95, -130, 20}},
        {"Hedge", {92, 68, 18, -20, 55}},
        {"PreserveOption", {72, 62, 42, 18, 70}},
        {"AdaptivePathway", {95, 72, 34, 10, 78}}
    };

    for (const auto& strategy : strategies) {
        std::cout << strategy.first << " robustness = "
                  << robustness(strategy.second, 40.0) << "\n";
    }

    return 0;
}
