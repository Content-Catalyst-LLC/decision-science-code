// regret_matrix_core.cpp
// Compile with: g++ -std=c++17 regret_matrix_core.cpp -o regret_matrix_core

#include <algorithm>
#include <iostream>
#include <vector>

double regret(double value, double scenario_best) {
    return scenario_best - value;
}

int main() {
    std::cout << "Regret = " << regret(0.72, 0.91) << "\n";
    return 0;
}
