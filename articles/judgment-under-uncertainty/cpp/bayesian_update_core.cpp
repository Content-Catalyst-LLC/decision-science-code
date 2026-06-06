// bayesian_update_core.cpp
// Compile with: g++ -std=c++17 bayesian_update_core.cpp -o bayesian_update_core

#include <iostream>

double posterior_from_likelihoods(double prior, double likelihood_true, double likelihood_false) {
    double odds = prior / (1.0 - prior);
    double posterior_odds = odds * (likelihood_true / likelihood_false);
    return posterior_odds / (1.0 + posterior_odds);
}

int main() {
    std::cout << "Posterior = " << posterior_from_likelihoods(0.35, 0.72, 0.28) << "\n";
    return 0;
}
