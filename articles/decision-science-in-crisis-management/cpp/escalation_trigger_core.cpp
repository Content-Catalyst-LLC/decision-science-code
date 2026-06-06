#include <iostream>

bool escalation_required(double risk, double uncertainty, double public_trust, double resource_pressure, double cascading_impact) {
    return risk >= 0.72 || uncertainty >= 0.62 || public_trust <= 0.46 || resource_pressure >= 0.70 || cascading_impact >= 0.64;
}

int main() {
    std::cout << "Escalation required = " << escalation_required(0.68, 0.64, 0.55, 0.61, 0.58) << "\n";
    return 0;
}
