// regret_matrix_solver.cpp
// Compile with: g++ -std=c++17 regret_matrix_solver.cpp -o regret_matrix_solver

#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

int main() {
    std::vector<std::string> names{"Optimize", "Hedge", "Preserve Option"};
    std::vector<std::vector<double>> payoff{
        {120.0, 25.0, -80.0},
        {90.0, 62.0, 12.0},
        {66.0, 58.0, 42.0}
    };

    std::vector<double> max_regrets(names.size(), 0.0);

    for (std::size_t scenario = 0; scenario < payoff[0].size(); ++scenario) {
        double best = payoff[0][scenario];
        for (std::size_t alt = 1; alt < payoff.size(); ++alt) {
            best = std::max(best, payoff[alt][scenario]);
        }

        for (std::size_t alt = 0; alt < payoff.size(); ++alt) {
            double regret = best - payoff[alt][scenario];
            max_regrets[alt] = std::max(max_regrets[alt], regret);
        }
    }

    for (std::size_t i = 0; i < names.size(); ++i) {
        std::cout << names[i] << " max regret = " << max_regrets[i] << "\n";
    }

    return 0;
}
