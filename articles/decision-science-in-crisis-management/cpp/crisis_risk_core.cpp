#include <iostream>

double crisis_risk(double likelihood, double severity, double exposure, double vulnerability, double criticality) {
    return likelihood * severity * exposure * vulnerability * criticality;
}

int main() {
    std::cout << "Crisis risk = " << crisis_risk(0.72, 0.86, 0.68, 0.62, 0.90) << "\n";
    return 0;
}
