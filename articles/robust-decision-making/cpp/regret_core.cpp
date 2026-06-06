#include <algorithm>
#include <iostream>
#include <vector>
double max_regret(const std::vector<double>& values, const std::vector<double>& bests) { double m = 0.0; for (size_t i = 0; i < values.size(); ++i) m = std::max(m, bests[i] - values[i]); return m; }
int main() { std::vector<double> values = {0.73, 0.77, 0.79, 0.81}; std::vector<double> bests = {0.92, 0.77, 0.83, 0.81}; std::cout << "Maximum regret = " << max_regret(values, bests) << "\n"; return 0; }
