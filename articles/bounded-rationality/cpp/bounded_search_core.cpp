// bounded_search_core.cpp
// Compile with: g++ -std=c++17 bounded_search_core.cpp -o bounded_search_core

#include <iostream>
#include <optional>
#include <utility>
#include <vector>

std::optional<std::pair<int, double>> first_satisficing(const std::vector<double>& values, double aspiration) {
    for (size_t i = 0; i < values.size(); ++i) {
        if (values[i] >= aspiration) {
            return std::make_pair(static_cast<int>(i + 1), values[i]);
        }
    }
    return std::nullopt;
}

int main() {
    std::vector<double> values{0.58, 0.71, 0.82, 0.77, 0.91};
    auto result = first_satisficing(values, 0.75);
    if (result) {
        std::cout << "Satisficing option = " << result->first << " value = " << result->second << "\n";
    } else {
        std::cout << "No option satisfies aspiration.\n";
    }
    return 0;
}
