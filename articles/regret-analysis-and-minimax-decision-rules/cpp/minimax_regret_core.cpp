// minimax_regret_core.cpp
// Compile with: g++ -std=c++17 minimax_regret_core.cpp -o minimax_regret_core

#include <algorithm>
#include <iostream>
#include <vector>

double max_regret(const std::vector<double>& regrets) {
    return *std::max_element(regrets.begin(), regrets.end());
}

int main() {
    std::vector<double> regrets = {0.19, 0.00, 0.05, 0.01, 0.06, 0.06};
    std::cout << "Maximum regret = " << max_regret(regrets) << "\n";
    return 0;
}
