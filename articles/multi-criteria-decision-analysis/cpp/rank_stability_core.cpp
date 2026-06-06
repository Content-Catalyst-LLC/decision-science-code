// rank_stability_core.cpp
// Compile with: g++ -std=c++17 rank_stability_core.cpp -o rank_stability_core

#include <iostream>
#include <vector>

double best_rank_rate(const std::vector<int>& ranks) {
    int count = 0;
    for (int rank : ranks) {
        if (rank == 1) {
            count++;
        }
    }
    return static_cast<double>(count) / ranks.size();
}

int main() {
    std::vector<int> ranks = {1, 1, 2, 3, 1, 2};
    std::cout << "Best-rank rate = " << best_rank_rate(ranks) << "\n";
    return 0;
}
