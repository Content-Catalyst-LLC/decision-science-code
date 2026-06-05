// expected_loss_core.cpp
// Compile with: g++ -std=c++17 expected_loss_core.cpp -o expected_loss_core

#include <iostream>
#include <vector>

double expected_loss(const std::vector<double>& probabilities, const std::vector<double>& losses) {
    double total = 0.0;
    for (std::size_t i = 0; i < probabilities.size(); ++i) {
        total += probabilities[i] * losses[i];
    }
    return total;
}

int main() {
    std::vector<double> probabilities{0.08, 0.06, 0.03};
    std::vector<double> losses{0.035, 0.040, 0.075};

    std::cout << "Expected loss = " << expected_loss(probabilities, losses) << "\n";
    return 0;
}
