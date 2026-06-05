// crra_expected_utility.cpp
// Compile with: g++ -std=c++17 crra_expected_utility.cpp -o crra_expected_utility

#include <cmath>
#include <iostream>
#include <vector>

double crra(double x, double rho, double offset = 151.0) {
    double z = x + offset;
    if (std::abs(rho - 1.0) < 1e-9) {
        return std::log(z);
    }
    return (std::pow(z, 1.0 - rho) - 1.0) / (1.0 - rho);
}

double expected_utility(const std::vector<double>& outcomes, const std::vector<double>& probabilities, double rho) {
    double total = 0.0;
    for (std::size_t i = 0; i < outcomes.size(); ++i) {
        total += probabilities[i] * crra(outcomes[i], rho);
    }
    return total;
}

int main() {
    std::vector<double> outcomes{180.0, 40.0};
    std::vector<double> probabilities{0.60, 0.40};
    std::cout << "Expected utility rho=1 = " << expected_utility(outcomes, probabilities, 1.0) << "\n";
    return 0;
}
