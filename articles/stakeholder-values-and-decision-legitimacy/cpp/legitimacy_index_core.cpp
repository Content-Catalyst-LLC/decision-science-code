// legitimacy_index_core.cpp
// Compile with: g++ -std=c++17 legitimacy_index_core.cpp -o legitimacy_index_core

#include <iostream>

double legitimacy_index(double aggregate_score, double procedural_score, double pass_rate, double min_score, double max_burden) {
    return 0.40 * aggregate_score + 0.24 * procedural_score + 0.18 * pass_rate + 0.10 * min_score - 0.08 * max_burden;
}

int main() {
    std::cout << "Legitimacy index = " << legitimacy_index(0.82, 0.89, 1.0, 0.76, 0.26) << "\n";
    return 0;
}
