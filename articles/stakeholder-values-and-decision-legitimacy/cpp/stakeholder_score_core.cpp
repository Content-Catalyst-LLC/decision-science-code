// stakeholder_score_core.cpp
// Compile with: g++ -std=c++17 stakeholder_score_core.cpp -o stakeholder_score_core

#include <iostream>
#include <vector>

double weighted_score(const std::vector<double>& values, const std::vector<double>& weights) {
    double total = 0.0;
    for (size_t i = 0; i < values.size(); ++i) {
        total += values[i] * weights[i];
    }
    return total;
}

int main() {
    std::vector<double> values = {0.68, 0.80, 0.84, 0.82, 0.86, 0.90};
    std::vector<double> weights = {0.12, 0.18, 0.28, 0.14, 0.16, 0.12};
    std::cout << "Stakeholder score = " << weighted_score(values, weights) << "\n";
    return 0;
}
