// regret_core.cpp
// Compile with: g++ -std=c++17 regret_core.cpp -o regret_core

#include <iostream>

double regret(double score, double best_score) {
    return best_score - score;
}

int main() {
    std::cout << "Regret = " << regret(0.72, 0.91) << "\n";
    return 0;
}
