// Compile with: g++ -std=c++17 legitimacy_core.cpp -o legitimacy_core
#include <iostream>
double legitimacy(double t, double p, double c, double a) { return 0.26*t + 0.24*p + 0.25*c + 0.25*a; }
int main() { std::cout << "Legitimacy = " << legitimacy(0.82, 0.80, 0.86, 0.90) << "\n"; return 0; }
