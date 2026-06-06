// feedback_loop_core.cpp
// Compile with: g++ -std=c++17 feedback_loop_core.cpp -o feedback_loop_core

#include <iostream>

double feedback_update(double state, double reinforcing, double balancing, double disturbance) {
    return state + reinforcing - balancing + disturbance;
}

int main() {
    std::cout << "Next state = " << feedback_update(55.0, 3.85, 2.10, -0.4) << "\n";
    return 0;
}
