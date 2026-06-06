// cosine_alignment_core.cpp
// Compile with: g++ -std=c++17 cosine_alignment_core.cpp -o cosine_alignment_core

#include <cmath>
#include <iostream>
#include <vector>

double cosine_similarity(const std::vector<double>& a, const std::vector<double>& b) {
    double dot = 0.0;
    double norm_a = 0.0;
    double norm_b = 0.0;

    for (size_t i = 0; i < a.size(); ++i) {
        dot += a[i] * b[i];
        norm_a += a[i] * a[i];
        norm_b += b[i] * b[i];
    }

    return dot / (std::sqrt(norm_a) * std::sqrt(norm_b));
}

int main() {
    std::vector<double> a = {0.68, 0.88, 0.82, 0.93, 0.86};
    std::vector<double> s = {0.20, 0.25, 0.18, 0.22, 0.15};
    std::cout << "Cosine alignment = " << cosine_similarity(a, s) << "\n";
    return 0;
}
