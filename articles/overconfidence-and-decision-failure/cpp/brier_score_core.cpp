// brier_score_core.cpp
// Compile with: g++ -std=c++17 brier_score_core.cpp -o brier_score_core

#include <cmath>
#include <iostream>

double brier_score(double probability, double outcome) {
    return std::pow(probability - outcome, 2.0);
}

double confidence_error(double confidence, double accuracy_proxy) {
    return confidence - accuracy_proxy;
}

int main() {
    std::cout << "Brier score = " << brier_score(0.69, 0.0) << "\n";
    std::cout << "Confidence error = " << confidence_error(0.88, 0.52) << "\n";
    return 0;
}
