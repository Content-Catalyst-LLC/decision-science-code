// robust_principle_score.cpp
// Compile with: g++ -std=c++17 robust_principle_score.cpp -o robust_principle_score

#include <algorithm>
#include <iostream>
#include <numeric>
#include <string>
#include <vector>

double mean(const std::vector<double>& values) {
    return std::accumulate(values.begin(), values.end(), 0.0) / values.size();
}

int main() {
    std::vector<double> scores{0.88, 0.87, 0.85, 0.84, 0.86, 0.86, 0.93, 0.84, 0.88};
    double composite = mean(scores);
    double minimum_score = *std::min_element(scores.begin(), scores.end());
    double robust_score = 0.70 * composite + 0.30 * minimum_score;

    std::cout << "Robust principle score = " << robust_score << "\n";
    return 0;
}
