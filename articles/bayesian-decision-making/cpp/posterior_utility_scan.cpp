// posterior_utility_scan.cpp
// Compile with: g++ -std=c++17 posterior_utility_scan.cpp -o posterior_utility_scan

#include <iostream>

double posterior_expected_utility(double posterior, double utility_true, double utility_false) {
    return posterior * utility_true + (1.0 - posterior) * utility_false;
}

int main() {
    double posterior = 0.443299;
    std::cout << "Action utility = " << posterior_expected_utility(posterior, 90.0, -25.0) << "\n";
    std::cout << "Wait utility = " << posterior_expected_utility(posterior, -80.0, 15.0) << "\n";
    return 0;
}
