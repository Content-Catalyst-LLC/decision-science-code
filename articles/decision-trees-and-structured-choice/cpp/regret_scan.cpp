// regret_scan.cpp
// Compile with: g++ -std=c++17 regret_scan.cpp -o regret_scan

#include <iostream>

double regret(double action_value, double best_state_value) {
    return best_state_value - action_value;
}

int main() {
    std::cout << "Example regret = " << regret(57.8, 75.1) << "\n";
    return 0;
}
