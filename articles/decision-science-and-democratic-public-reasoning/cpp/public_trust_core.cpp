// public_trust_core.cpp
// Compile with: g++ -std=c++17 public_trust_core.cpp -o public_trust_core

#include <algorithm>
#include <iostream>

double next_trust(double current, double performance, double transparency, double responsiveness, double fairness, double uncertainty, double harm) {
    return std::clamp(current + 0.08 * performance + 0.06 * transparency + 0.08 * responsiveness + 0.08 * fairness - 0.06 * uncertainty - 0.10 * harm, 0.0, 1.0);
}

int main() {
    std::cout << "Next trust = " << next_trust(0.62, 0.70, 0.78, 0.74, 0.72, 0.36, 0.30) << "\n";
    return 0;
}
