// historical_minimax_regret_solver.cpp
// Compile with: g++ -std=c++17 historical_minimax_regret_solver.cpp -o historical_minimax_regret_solver

#include <algorithm>
#include <iostream>
#include <limits>
#include <string>
#include <vector>

int main() {
    std::vector<std::string> names{"Aggressive", "Balanced", "Defensive", "Adaptive"};
    std::vector<std::vector<double>> payoff{
        {128, 50, -90, -20},
        {92, 68, 18, 42},
        {62, 58, 44, 54},
        {88, 70, 36, 72}
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
