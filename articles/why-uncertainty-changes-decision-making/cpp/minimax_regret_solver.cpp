// minimax_regret_solver.cpp
// Compile with: g++ -std=c++17 minimax_regret_solver.cpp -o minimax_regret_solver

#include <algorithm>
#include <iostream>
#include <limits>
#include <string>
#include <vector>

int main() {
    std::vector<std::string> names{"Expand", "Hedge", "PreserveOption", "AdaptivePathway"};
    std::vector<std::vector<double>> payoff{
        {120, 45, -95, -130, 20},
        {92, 68, 18, -20, 55},
        {72, 62, 42, 18, 70},
        {95, 72, 34, 10, 78}
    };

    std::vector<double> max_regrets(names.size(), 0.0);

    for (std::size_t scenario = 0; scenario < payoff[0].size(); ++scenario) {
        double best = -std::numeric_limits<double>::infinity();
        for (const auto& row : payoff) {
            best = std::max(best, row[scenario]);
        }
        for (std::size_t alt = 0; alt < payoff.size(); ++alt) {
            max_regrets[alt] = std::max(max_regrets[alt], best - payoff[alt][scenario]);
        }
    }

    for (std::size_t i = 0; i < names.size(); ++i) {
        std::cout << names[i] << " max regret = " << max_regrets[i] << "\n";
    }

    return 0;
}
