// sensitivity_weight_scan.cpp
// Compile with: g++ -std=c++17 sensitivity_weight_scan.cpp -o sensitivity_weight_scan

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
    std::vector<double> scores{0.88, 0.87, 0.85, 0.84, 0.86, 0.86, 0.93, 0.84, 0.88};
    std::vector<double> weights{0.12, 0.14, 0.12, 0.10, 0.11, 0.14, 0.12, 0.08, 0.07};

    std::cout << "Base score = " << weighted_score(scores, weights) << "\n";
    return 0;
}
