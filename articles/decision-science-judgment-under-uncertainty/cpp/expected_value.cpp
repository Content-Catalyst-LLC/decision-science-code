#include <iostream>
#include <vector>

struct Outcome {
    double probability;
    double value;
};

double expected_value(const std::vector<Outcome>& outcomes) {
    double total = 0.0;

    for (const auto& outcome : outcomes) {
        total += outcome.probability * outcome.value;
    }

    return total;
}

int main() {
    std::vector<Outcome> outcomes = {
        {0.65, 72.0},
        {0.35, 38.0}
    };

    std::cout << "Expected value: " << expected_value(outcomes) << "\n";

    return 0;
}
