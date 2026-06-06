// future_maturity_core.cpp
// Compile with: g++ -std=c++17 future_maturity_core.cpp -o future_maturity_core

#include <algorithm>
#include <iostream>

double future_maturity(double ai, double governance, double uncertainty, double legitimacy, double reproducibility, double systems, double ethics, double adaptive, double failure) {
    return std::clamp(0.12 * ai + 0.14 * governance + 0.14 * uncertainty + 0.12 * legitimacy + 0.12 * reproducibility + 0.12 * systems + 0.14 * ethics + 0.14 * adaptive - 0.14 * failure, 0.0, 1.0);
}

int main() {
    std::cout << "Future maturity = " << future_maturity(0.86, 0.90, 0.88, 0.84, 0.88, 0.86, 0.90, 0.88, 0.24) << "\n";
    return 0;
}
