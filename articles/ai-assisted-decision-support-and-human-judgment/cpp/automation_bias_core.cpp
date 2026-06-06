// automation_bias_core.cpp
// Compile with: g++ -std=c++17 automation_bias_core.cpp -o automation_bias_core

#include <iostream>

double automation_bias(double actual_reliance, double justified_reliance) {
    return actual_reliance - justified_reliance;
}

int main() {
    std::cout << "Automation bias = " << automation_bias(0.78, 0.56) << "\n";
    return 0;
}
