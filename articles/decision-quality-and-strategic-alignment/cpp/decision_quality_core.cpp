// decision_quality_core.cpp
// Compile with: g++ -std=c++17 decision_quality_core.cpp -o decision_quality_core

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
    std::vector<double> scores = {0.86, 0.88, 0.82, 0.86, 0.89, 0.77};
    std::vector<double> weights = {0.16, 0.15, 0.17, 0.18, 0.18, 0.16};
    std::cout << "Decision quality score = " << weighted_score(scores, weights) << "\n";
    return 0;
}
