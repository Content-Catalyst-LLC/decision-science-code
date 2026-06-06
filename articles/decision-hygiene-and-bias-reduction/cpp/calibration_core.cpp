// calibration_core.cpp
// Compile with: g++ -std=c++17 calibration_core.cpp -o calibration_core

#include <cmath>
#include <iostream>

double brier_score(double probability, double outcome) {
    return std::pow(probability - outcome, 2.0);
}

double calibration_gap(double predicted, double observed) {
    return predicted - observed;
}

int main() {
    std::cout << "Brier score = " << brier_score(0.69, 0.0) << "\n";
    std::cout << "Calibration gap = " << calibration_gap(0.75, 0.62) << "\n";
    return 0;
}
