// cascade_risk_core.cpp
// Compile with: g++ -std=c++17 cascade_risk_core.cpp -o cascade_risk_core

#include <iostream>

double cascade_risk_score(double exposure, double dependency_centrality, double buffer_weakness, double common_mode_risk, double monitoring_quality, double response_capacity) {
    return 0.22 * exposure + 0.22 * dependency_centrality + 0.20 * buffer_weakness + 0.18 * common_mode_risk - 0.09 * monitoring_quality - 0.09 * response_capacity;
}

int main() {
    std::cout << "Cascade risk score = " << cascade_risk_score(0.82, 0.88, 0.76, 0.79, 0.42, 0.40) << "\n";
    return 0;
}
