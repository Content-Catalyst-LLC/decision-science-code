// bayes_update_core.cpp
// Compile with: g++ -std=c++17 bayes_update_core.cpp -o bayes_update_core

#include <iostream>

double bayesian_update(double prior, double sensitivity, double false_positive_rate) {
    double numerator = sensitivity * prior;
    double denominator = numerator + false_positive_rate * (1.0 - prior);
    return numerator / denominator;
}

int main() {
    std::cout << "Posterior = " << bayesian_update(0.10, 0.86, 0.12) << "\n";
    return 0;
}
