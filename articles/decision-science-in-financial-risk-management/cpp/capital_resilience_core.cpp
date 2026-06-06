// capital_resilience_core.cpp
// Compile with: g++ -std=c++17 capital_resilience_core.cpp -o capital_resilience_core

#include <algorithm>
#include <iostream>

double capital_next(double current_capital, double period_return_pct, double floor) {
    return std::max(floor, current_capital * (1.0 + period_return_pct / 100.0));
}

int main() {
    std::cout << "Capital next = " << capital_next(100.0, -8.5, 20.0) << "\n";
    return 0;
}
