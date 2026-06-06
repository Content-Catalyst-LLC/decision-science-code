// pathway_score_core.cpp
// Compile with: g++ -std=c++17 pathway_score_core.cpp -o pathway_score_core

#include <iostream>

double pathway_score(double initial_performance, double flexibility, double monitoring_quality, double trigger_clarity, double switching_cost, double fallback_strength) {
    return 0.20 * initial_performance + 0.18 * flexibility + 0.16 * monitoring_quality + 0.16 * trigger_clarity - 0.12 * switching_cost + 0.18 * fallback_strength;
}

int main() {
    std::cout << "Pathway score = " << pathway_score(0.76, 0.88, 0.82, 0.80, 0.38, 0.84) << "\n";
    return 0;
}
