// aspiration_update_core.cpp
// Compile with: g++ -std=c++17 aspiration_update_core.cpp -o aspiration_update_core

#include <algorithm>
#include <iostream>

double update_aspiration(double current, double feedback, double learning_rate) {
    return std::clamp(current + learning_rate * (feedback - current), 0.35, 0.95);
}

int main() {
    double aspiration = 0.70;
    for (double feedback : {0.74, 0.68, 0.76}) {
        aspiration = update_aspiration(aspiration, feedback, 0.12);
        std::cout << "Aspiration = " << aspiration << "\n";
    }
    return 0;
}
