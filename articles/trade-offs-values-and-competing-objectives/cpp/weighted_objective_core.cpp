// weighted_objective_core.cpp
// Compile with: g++ -std=c++17 weighted_objective_core.cpp -o weighted_objective_core

#include <iostream>
#include <vector>

double weighted_score(const std::vector<double>& scores, const std::vector<double>& weights) {
    double total = 0.0;
    for (size_t i = 0; i < scores.size(); ++i) {
        total += scores[i] * weights[i];
    }
    return total;
}

int main() {
    std::vector<double> scores = {0.90, 0.38, 0.42, 0.54, 0.48, 0.70};
    std::vector<double> weights = {0.18, 0.18, 0.20, 0.18, 0.14, 0.12};
    std::cout << "Weighted score = " << weighted_score(scores, weights) << "\n";
    return 0;
}
