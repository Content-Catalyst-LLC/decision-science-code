// responsibility_gap_core.cpp
// Compile with: g++ -std=c++17 responsibility_gap_core.cpp -o responsibility_gap_core

#include <algorithm>
#include <iostream>

double responsibility_gap(double influence, double accountability) {
    return std::max(0.0, influence - accountability);
}

int main() {
    std::cout << "Responsibility gap = " << responsibility_gap(0.62, 0.34) << "\n";
    return 0;
}
