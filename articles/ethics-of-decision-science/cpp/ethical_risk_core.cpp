// Compile with: g++ -std=c++17 ethical_risk_core.cpp -o ethical_risk_core
#include <algorithm>
#include <iostream>
double ethical_risk(double h, double o, double e, double i, double a) { return std::clamp(0.30*h + 0.20*o + 0.22*e + 0.18*i - 0.10*a, 0.0, 1.0); }
int main() { std::cout << "Ethical risk = " << ethical_risk(0.64, 0.58, 0.68, 0.56, 0.46) << "\n"; return 0; }
