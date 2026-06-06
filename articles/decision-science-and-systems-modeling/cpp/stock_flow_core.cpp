// stock_flow_core.cpp
// Compile with: g++ -std=c++17 stock_flow_core.cpp -o stock_flow_core

#include <iostream>

double stock_update(double stock, double inflow, double outflow) {
    return stock + inflow - outflow;
}

int main() {
    std::cout << "Next stock = " << stock_update(100.0, 12.0, 8.5) << "\n";
    return 0;
}
