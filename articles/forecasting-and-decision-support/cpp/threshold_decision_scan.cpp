// threshold_decision_scan.cpp
// Compile with: g++ -std=c++17 threshold_decision_scan.cpp -o threshold_decision_scan

#include <iostream>

double threshold_from_costs(double false_positive_cost, double false_negative_cost) {
    return false_positive_cost / (false_positive_cost + false_negative_cost);
}

int main() {
    std::cout << "Threshold = " << threshold_from_costs(15.0, 85.0) << "\n";
    return 0;
}
