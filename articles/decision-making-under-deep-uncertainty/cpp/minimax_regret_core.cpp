// minimax_regret_core.cpp
// Compile with: g++ -std=c++17 minimax_regret_core.cpp -o minimax_regret_core

#include <algorithm>
#include <iostream>
#include <vector>

double max_regret(const std::vector<double>& values, const std::vector<double>& scenario_bests) {
    double max_value = 0.0;
    for (size_t i = 0; i < values.size(); ++i) {
        max_value = std::max(max_value, scenario_bests[i] - values[i]);
    }
    return max_value;
}

int main() {
    std::vector<double> values = {0.72, 0.80, 0.78, 0.87, 0.75, 0.77};
    std::vector<double> bests = {0.91, 0.80, 0.84, 0.88, 0.81, 0.83};
    std::cout << "Maximum regret = " << max_regret(values, bests) << "\n";
    return 0;
}
