// record_quality_score.cpp
// Compile with: g++ -std=c++17 record_quality_score.cpp -o record_quality_score

#include <algorithm>
#include <iostream>
#include <numeric>
#include <vector>

double weighted_score(const std::vector<double>& scores, const std::vector<double>& weights) {
    double total = 0.0;
    for (std::size_t i = 0; i < scores.size(); ++i) {
        total += scores[i] * weights[i];
    }
    return total;
}

int main() {
    std::vector<double> weights{0.10,0.09,0.11,0.11,0.12,0.10,0.09,0.10,0.09,0.09,0.10};
    std::vector<double> record{0.91,0.88,0.80,0.89,0.92,0.86,0.84,0.88,0.90,0.92,0.90};

    double quality = weighted_score(record, weights);
    double minimum_component = *std::min_element(record.begin(), record.end());
    double accountable = 0.70 * quality + 0.30 * minimum_component;

    std::cout << "Accountable judgment score = " << accountable << "\n";
    return 0;
}
