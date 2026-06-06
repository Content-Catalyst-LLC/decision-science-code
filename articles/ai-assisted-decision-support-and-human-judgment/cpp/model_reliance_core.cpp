// model_reliance_core.cpp
// Compile with: g++ -std=c++17 model_reliance_core.cpp -o model_reliance_core

#include <algorithm>
#include <iostream>

double justified_model_reliance(double evidence_quality, double calibration, double decision_risk, double uncertainty) {
    return std::clamp(0.35 * evidence_quality + 0.35 * calibration - 0.16 * decision_risk - 0.14 * uncertainty, 0.0, 1.0);
}

int main() {
    std::cout << "Justified model reliance = " << justified_model_reliance(0.82, 0.78, 0.54, 0.36) << "\n";
    return 0;
}
