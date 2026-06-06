// bias_noise_core.cpp
// Compile with: g++ -std=c++17 bias_noise_core.cpp -o bias_noise_core

#include <iostream>
#include <numeric>
#include <vector>

double bias(const std::vector<double>& errors) {
    return std::accumulate(errors.begin(), errors.end(), 0.0) / errors.size();
}

double mse(const std::vector<double>& errors) {
    double total = 0.0;
    for (double error : errors) {
        total += error * error;
    }
    return total / errors.size();
}

int main() {
    std::vector<double> errors = {0.12, 0.04, -0.03, 0.08};
    std::cout << "Bias = " << bias(errors) << "\n";
    std::cout << "MSE = " << mse(errors) << "\n";
    return 0;
}
