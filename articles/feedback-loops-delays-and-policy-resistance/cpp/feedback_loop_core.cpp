// feedback_loop_core.cpp
// Compile with: g++ -std=c++17 feedback_loop_core.cpp -o feedback_loop_core

#include <iostream>

double feedback_update(double state, double reinforcing, double balancing, double resistance, double disturbance) {
    return state + reinforcing - balancing + resistance + disturbance;
}

int main() {
    std::cout << "Next state = " << feedback_update(50.0, 4.0, 1.12, 0.4, -0.3) << "\n";
    return 0;
}
