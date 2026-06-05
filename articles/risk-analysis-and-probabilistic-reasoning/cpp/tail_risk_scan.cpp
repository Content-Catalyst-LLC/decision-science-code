// tail_risk_scan.cpp
// Compile with: g++ -std=c++17 tail_risk_scan.cpp -o tail_risk_scan

#include <algorithm>
#include <iostream>
#include <numeric>
#include <vector>

double quantile(std::vector<double> values, double probability) {
    std::sort(values.begin(), values.end());
    std::size_t index = static_cast<std::size_t>(probability * (values.size() - 1));
    return values[index];
}

int main() {
    std::vector<double> returns{0.04, 0.02, -0.03, 0.08, -0.12, 0.01, -0.20, 0.06};
    double var_5 = quantile(returns, 0.05);
    std::cout << "VaR 5pct = " << var_5 << "\n";
    return 0;
}
