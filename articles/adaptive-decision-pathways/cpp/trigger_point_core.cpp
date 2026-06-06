// trigger_point_core.cpp
// Compile with: g++ -std=c++17 trigger_point_core.cpp -o trigger_point_core

#include <iostream>

bool trigger_hit(double system_stress, double option_value, double stress_trigger, double option_value_trigger) {
    return system_stress >= stress_trigger || option_value <= option_value_trigger;
}

int main() {
    std::cout << "Trigger hit? " << trigger_hit(0.70, 0.55, 0.68, 0.40) << "\n";
    return 0;
}
