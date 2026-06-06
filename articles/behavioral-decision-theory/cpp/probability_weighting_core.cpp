// probability_weighting_core.cpp
// Compile with: g++ -std=c++17 probability_weighting_core.cpp -o probability_weighting_core

#include <cmath>
#include <iostream>

double weighted_probability(double p, double gamma) {
    return std::pow(p, gamma) / std::pow(std::pow(p, gamma) + std::pow(1.0 - p, gamma), 1.0 / gamma);
}

int main() {
    std::cout << "Weighted probability = " << weighted_probability(0.10, 0.72) << "\n";
    return 0;
}
