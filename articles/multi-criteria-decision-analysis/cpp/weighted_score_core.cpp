// weighted_score_core.cpp
// Compile with: g++ -std=c++17 weighted_score_core.cpp -o weighted_score_core

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
    std::vector<double> scores = {0.8, 0.6, 0.9};
    std::vector<double> weights = {0.3, 0.3, 0.4};
    std::cout << "Weighted score = " << weighted_score(scores, weights) << "\n";
    return 0;
}
