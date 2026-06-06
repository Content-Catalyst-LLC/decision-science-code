// adaptive_trigger_core.cpp
// Compile with: g++ -std=c++17 adaptive_trigger_core.cpp -o adaptive_trigger_core

#include <iostream>

bool trigger_reached(double indicator, double threshold) {
    return indicator >= threshold;
}

int main() {
    std::cout << "Adaptive trigger reached = " << trigger_reached(0.74, 0.70) << "\n";
    return 0;
}
