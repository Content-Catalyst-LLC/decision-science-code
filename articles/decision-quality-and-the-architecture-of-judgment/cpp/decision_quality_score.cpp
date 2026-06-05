// decision_quality_score.cpp
// Compile with: g++ -std=c++17 decision_quality_score.cpp -o decision_quality_score

#include <iostream>
#include <vector>

double weighted_score(const std::vector<double>& scores, const std::vector<double>& weights) {
    double total = 0.0;
    for (std::size_t i = 0; i < scores.size(); ++i) {
        total += scores[i] * weights[i];
    }
    return total;
}

int main() {
    std::vector<double> weights{0.11,0.10,0.12,0.13,0.11,0.10,0.11,0.11,0.11};
    std::vector<double> staged{0.92,0.90,0.94,0.90,0.88,0.86,0.82,0.94,0.96};

    std::cout << "Staged Learning Decision quality = "
              << weighted_score(staged, weights) << "\n";

    return 0;
}
