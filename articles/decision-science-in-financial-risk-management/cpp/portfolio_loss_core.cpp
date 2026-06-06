// portfolio_loss_core.cpp
// Compile with: g++ -std=c++17 portfolio_loss_core.cpp -o portfolio_loss_core

#include <iostream>
#include <vector>

double expected_loss(const std::vector<double>& losses, const std::vector<double>& probabilities) {
    double total = 0.0;
    for (std::size_t i = 0; i < losses.size(); ++i) {
        total += losses[i] * probabilities[i];
    }
    return total;
}

int main() {
    std::vector<double> losses{-1.2, -4.8, -3.6, -6.2};
    std::vector<double> probabilities{0.55, 0.20, 0.15, 0.10};
    std::cout << "Expected loss = " << expected_loss(losses, probabilities) << "\n";
    return 0;
}
