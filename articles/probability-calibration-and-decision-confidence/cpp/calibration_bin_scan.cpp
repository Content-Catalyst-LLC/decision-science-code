// calibration_bin_scan.cpp
// Compile with: g++ -std=c++17 calibration_bin_scan.cpp -o calibration_bin_scan

#include <iostream>
#include <vector>
#include <numeric>

double mean(const std::vector<double>& values) {
    return std::accumulate(values.begin(), values.end(), 0.0) / values.size();
}

int main() {
    std::vector<double> probabilities{0.72, 0.76, 0.79};
    std::vector<double> outcomes{1.0, 1.0, 0.0};

    std::cout << "Calibration gap = " << mean(probabilities) - mean(outcomes) << "\n";
    return 0;
}
