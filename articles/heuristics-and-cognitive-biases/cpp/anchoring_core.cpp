// anchoring_core.cpp
// Compile with: g++ -std=c++17 anchoring_core.cpp -o anchoring_core

#include <iostream>
#include <cmath>

double anchored_estimate(double anchor, double evidence, double weight) {
    return weight * anchor + (1.0 - weight) * evidence;
}

int main() {
    std::cout << "Anchored estimate = " << anchored_estimate(0.80, 0.42, 0.45) << "\n";
    return 0;
}
