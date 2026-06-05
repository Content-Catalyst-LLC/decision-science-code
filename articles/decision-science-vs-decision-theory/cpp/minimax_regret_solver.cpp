// minimax_regret_solver.cpp
// Compile with: g++ -std=c++17 minimax_regret_solver.cpp -o minimax_regret_solver

#include <algorithm>
#include <iostream>
#include <limits>
#include <string>
#include <vector>

int main() {
    std::vector<std::string> names{"Optimize", "Balanced", "Robust", "Adaptive", "StagedPilot"};
    std::vector<std::vector<double>> payoff{
        {145, 92, 30, -95, -40},
        {112, 84, 58, 12, 30},
        {78, 72, 65, 48, 55},
        {98, 80, 62, 38, 68},
        {82, 70, 60, 42, 74}
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
