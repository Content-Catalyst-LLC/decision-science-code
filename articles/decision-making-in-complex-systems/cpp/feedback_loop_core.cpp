// feedback_loop_core.cpp
// Compile with: g++ -std=c++17 feedback_loop_core.cpp -o feedback_loop_core

#include <iostream>

double feedback_update(double state, double reinforcing, double balancing, double disturbance) {
    return state + reinforcing - balancing + disturbance;
}

int main() {
    std::cout << "Next state = " << feedback_update(52.0, 3.0, 1.4, -0.2) << "\n";
    return 0;
}
