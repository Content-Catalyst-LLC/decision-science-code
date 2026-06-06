// ai_risk_core.cpp
// Compile with: g++ -std=c++17 ai_risk_core.cpp -o ai_risk_core

#include <iostream>

double composite_ai_risk(double safety, double equity, double bias, double privacy, double opacity, double security) {
    return 0.20 * safety + 0.18 * equity + 0.16 * bias + 0.16 * privacy + 0.14 * opacity + 0.16 * security;
}

int main() {
    std::cout << "Composite AI risk = " << composite_ai_risk(0.52, 0.48, 0.50, 0.42, 0.55, 0.46) << "\n";
    return 0;
}
