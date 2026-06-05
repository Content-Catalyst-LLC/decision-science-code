// forecast_error_core.cpp
// Compile with: g++ -std=c++17 forecast_error_core.cpp -o forecast_error_core

#include <cmath>
#include <iostream>
#include <vector>

double mean_absolute_error(const std::vector<double>& actual, const std::vector<double>& forecast) {
    double total = 0.0;
    for (size_t i = 0; i < actual.size(); ++i) {
        total += std::abs(actual[i] - forecast[i]);
    }
    return total / actual.size();
}

double brier_score(double probability, double outcome) {
    return std::pow(probability - outcome, 2.0);
}

int main() {
    std::vector<double> actual{100.0, 112.0, 95.0, 121.0};
    std::vector<double> forecast{98.0, 108.0, 101.0, 119.0};
    std::cout << "MAE = " << mean_absolute_error(actual, forecast) << "\n";
    std::cout << "Brier score = " << brier_score(0.62, 1.0) << "\n";
    return 0;
}
