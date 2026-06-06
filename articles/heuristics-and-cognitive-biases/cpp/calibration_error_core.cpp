// calibration_error_core.cpp
// Compile with: g++ -std=c++17 calibration_error_core.cpp -o calibration_error_core

#include <iostream>
#include <cmath>

double brier_score(double probability, double outcome) {
    return std::pow(probability - outcome, 2.0);
}

int main() {
    std::cout << "Brier score = " << brier_score(0.72, 1.0) << "\n";
    return 0;
}
