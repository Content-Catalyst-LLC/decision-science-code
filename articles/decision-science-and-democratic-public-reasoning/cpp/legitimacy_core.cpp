// legitimacy_core.cpp
// Compile with: g++ -std=c++17 legitimacy_core.cpp -o legitimacy_core

#include <iostream>

double legitimacy_score(double transparency, double participation, double fairness, double evidence, double contestability, double accountability) {
    return 0.17 * transparency + 0.17 * participation + 0.18 * fairness + 0.16 * evidence + 0.16 * contestability + 0.16 * accountability;
}

int main() {
    std::cout << "Legitimacy score = " << legitimacy_score(0.88, 0.88, 0.88, 0.84, 0.86, 0.88) << "\n";
    return 0;
}
