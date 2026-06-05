// regret_scan.cpp
// Compile with: g++ -std=c++17 regret_scan.cpp -o regret_scan

#include <iostream>

double regret(double action_value, double best_value) {
    return best_value - action_value;
}

int main() {
    std::cout << "Regret = " << regret(68.0, 79.5) << "\n";
    return 0;
}
