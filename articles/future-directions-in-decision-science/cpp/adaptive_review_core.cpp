// adaptive_review_core.cpp
// Compile with: g++ -std=c++17 adaptive_review_core.cpp -o adaptive_review_core

#include <iostream>

bool review_required(double governance, double uncertainty, double ethics, double adaptive, double failure) {
    return governance <= 0.58 || uncertainty <= 0.58 || ethics <= 0.58 || adaptive <= 0.58 || failure >= 0.62;
}

int main() {
    std::cout << "Review required = " << review_required(0.54, 0.62, 0.50, 0.54, 0.56) << "\n";
    return 0;
}
