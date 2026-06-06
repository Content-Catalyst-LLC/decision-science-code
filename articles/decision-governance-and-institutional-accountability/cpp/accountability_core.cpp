// accountability_core.cpp
// Compile with: g++ -std=c++17 accountability_core.cpp -o accountability_core

#include <iostream>

double accountability_score(double decision_rights, double traceability, double review, double ownership, double monitoring, double corrective) {
    return 0.18 * decision_rights + 0.17 * traceability + 0.18 * review + 0.17 * ownership + 0.15 * monitoring + 0.15 * corrective;
}

int main() {
    std::cout << "Accountability score = " << accountability_score(0.82, 0.86, 0.88, 0.84, 0.90, 0.92) << "\n";
    return 0;
}
