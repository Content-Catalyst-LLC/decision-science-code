// brier_score_core.cpp
// Compile with: g++ -std=c++17 brier_score_core.cpp -o brier_score_core

#include <cmath>
#include <iostream>

double brier_score(double probability, double outcome) {
    return std::pow(probability - outcome, 2.0);
}

int main() {
    std::cout << "Brier score = " << brier_score(0.62, 1.0) << "\n";
    return 0;
}
