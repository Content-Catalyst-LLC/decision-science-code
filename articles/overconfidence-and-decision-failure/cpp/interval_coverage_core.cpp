// interval_coverage_core.cpp
// Compile with: g++ -std=c++17 interval_coverage_core.cpp -o interval_coverage_core

#include <iostream>

bool interval_hit(double lower, double upper, double actual) {
    return lower <= actual && actual <= upper;
}

int main() {
    std::cout << "Interval hit = " << interval_hit(90.0, 150.0, 154.0) << "\n";
    std::cout << "Interval hit = " << interval_hit(70.0, 110.0, 96.0) << "\n";
    return 0;
}
