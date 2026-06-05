// assumption_risk_scan.cpp
// Compile with: g++ -std=c++17 assumption_risk_scan.cpp -o assumption_risk_scan

#include <iostream>
#include <string>
#include <vector>

struct Assumption {
    std::string id;
    double confidence;
    double criticality;
};

int main() {
    std::vector<Assumption> assumptions{
        {"A1", 0.62, 0.86},
        {"A7", 0.42, 0.90},
        {"A8", 0.38, 0.84}
    };

    for (const auto& item : assumptions) {
        double risk = item.criticality * (1.0 - item.confidence);
        std::cout << item.id << " assumption risk = " << risk << "\n";
    }

    return 0;
}
