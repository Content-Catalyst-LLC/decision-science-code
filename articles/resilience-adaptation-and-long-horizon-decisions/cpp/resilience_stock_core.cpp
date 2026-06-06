// resilience_stock_core.cpp
// Compile with: g++ -std=c++17 resilience_stock_core.cpp -o resilience_stock_core

#include <algorithm>
#include <iostream>

double resilience_update(double current, double recovery, double investment, double degradation, double shock) {
    return std::max(0.0, current + recovery + investment - degradation - shock);
}

int main() {
    std::cout << "Next resilience stock = " << resilience_update(35.0, 3.0, 2.0, 1.0, 1.6) << "\n";
    return 0;
}
