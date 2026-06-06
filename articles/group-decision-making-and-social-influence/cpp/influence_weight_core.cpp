// influence_weight_core.cpp
// Compile with: g++ -std=c++17 influence_weight_core.cpp -o influence_weight_core

#include <algorithm>
#include <iostream>
#include <numeric>
#include <vector>

int main() {
    std::vector<double> values = {0.72, 0.61, 0.80, 0.47, 0.69, 0.58, 0.84};
    double total = std::accumulate(values.begin(), values.end(), 0.0);
    double max_weight = 0.0;
    for (double value : values) {
        max_weight = std::max(max_weight, value / total);
    }
    std::cout << "Influence concentration = " << max_weight << "\n";
    return 0;
}
