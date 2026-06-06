// prospect_value_core.cpp
// Compile with: g++ -std=c++17 prospect_value_core.cpp -o prospect_value_core

#include <cmath>
#include <iostream>

double prospect_value(double x, double alpha, double beta, double loss_aversion) {
    if (x >= 0.0) {
        return std::pow(x, alpha);
    }
    return -loss_aversion * std::pow(-x, beta);
}

int main() {
    std::cout << "Gain value = " << prospect_value(100.0, 0.88, 0.88, 2.0) << "\n";
    std::cout << "Loss value = " << prospect_value(-100.0, 0.88, 0.88, 2.0) << "\n";
    return 0;
}
