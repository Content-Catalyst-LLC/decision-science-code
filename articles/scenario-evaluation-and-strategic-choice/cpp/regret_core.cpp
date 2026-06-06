// regret_core.cpp
// Compile with: g++ -std=c++17 regret_core.cpp -o regret_core

#include <algorithm>
#include <iostream>
#include <vector>

double maximum_regret(const std::vector<double>& strategy_values, const std::vector<double>& scenario_best_values) {
    double max_regret = 0.0;
    for (std::size_t i = 0; i < strategy_values.size(); ++i) {
        max_regret = std::max(max_regret, scenario_best_values[i] - strategy_values[i]);
    }
    return max_regret;
}

int main() {
    std::vector<double> values{0.76, 0.71, 0.63};
    std::vector<double> best{0.92, 0.76, 0.82};
    std::cout << "Maximum regret = " << maximum_regret(values, best) << "\n";
    return 0;
}
