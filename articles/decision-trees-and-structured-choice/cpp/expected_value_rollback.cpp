// expected_value_rollback.cpp
// Compile with: g++ -std=c++17 expected_value_rollback.cpp -o expected_value_rollback

#include <iostream>

double expected_value(double success_payoff, double failure_payoff, double success_probability, double cost, double credit) {
    return success_payoff * success_probability + failure_payoff * (1.0 - success_probability) - cost + credit;
}

int main() {
    double immediate = expected_value(125.0, -35.0, 0.58, 0.0, 0.0);
    double staged = expected_value(145.0, -20.0, 0.54, 12.0, 18.0);

    std::cout << "Immediate EV = " << immediate << "\n";
    std::cout << "Staged EV = " << staged << "\n";
    std::cout << "Net value of staging = " << staged - immediate << "\n";
    return 0;
}
