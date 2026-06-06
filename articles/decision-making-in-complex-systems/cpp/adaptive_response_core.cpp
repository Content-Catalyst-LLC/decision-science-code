// adaptive_response_core.cpp
// Compile with: g++ -std=c++17 adaptive_response_core.cpp -o adaptive_response_core

#include <algorithm>
#include <iostream>

double adaptive_response_update(double response, double target, double current_state, double learning_rate) {
    return std::max(0.0, response + learning_rate * (target - current_state));
}

int main() {
    std::cout << "Adaptive response = " << adaptive_response_update(14.0, 58.0, 52.0, 0.06) << "\n";
    return 0;
}
