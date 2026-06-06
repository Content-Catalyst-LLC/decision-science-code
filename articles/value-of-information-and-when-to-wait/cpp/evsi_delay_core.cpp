// evsi_delay_core.cpp
// Compile with: g++ -std=c++17 evsi_delay_core.cpp -o evsi_delay_core

#include <iostream>

double evsi(double sample_information_value, double current_expected_value) {
    return sample_information_value - current_expected_value;
}

double net_value_waiting(double evsi_value, double information_cost, double delay_cost) {
    return evsi_value - information_cost - delay_cost;
}

int main() {
    double evsi_value = evsi(72.5, 68.1);
    std::cout << "EVSI = " << evsi_value << "\n";
    std::cout << "Net value waiting = " << net_value_waiting(evsi_value, 2.0, 1.3) << "\n";
    return 0;
}
