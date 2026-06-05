// outcome_bias_scan.cpp
// Compile with: g++ -std=c++17 outcome_bias_scan.cpp -o outcome_bias_scan

#include <iostream>
#include <string>

std::string classify(double process_score, double favorable_outcome_rate) {
    if (process_score < 0.60 && favorable_outcome_rate > 0.50) {
        return "possible luck masking weak process";
    }
    if (process_score >= 0.80 && favorable_outcome_rate < 0.50) {
        return "sound process exposed to unfavorable uncertainty";
    }
    return "process and outcome broadly aligned";
}

int main() {
    std::cout << classify(0.52, 0.70) << "\n";
    std::cout << classify(0.86, 0.42) << "\n";
    return 0;
}
