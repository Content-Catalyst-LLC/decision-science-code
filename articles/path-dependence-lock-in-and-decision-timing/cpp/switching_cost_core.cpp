// switching_cost_core.cpp
// Compile with: g++ -std=c++17 switching_cost_core.cpp -o switching_cost_core

#include <iostream>

double switching_cost(double investment, double network_dependence, double institutional_routine) {
    return 0.36 * investment + 0.34 * network_dependence + 0.30 * institutional_routine;
}

int main() {
    std::cout << "Switching cost = " << switching_cost(0.55, 0.62, 0.58) << "\n";
    return 0;
}
