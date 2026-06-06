// frame_reversal_scan.cpp
// Compile with: g++ -std=c++17 frame_reversal_scan.cpp -o frame_reversal_scan

#include <iostream>
#include <string>

bool frame_reversal(const std::string& gain_choice, const std::string& loss_choice) {
    return gain_choice != loss_choice;
}

int main() {
    std::cout << "Frame reversal: " << frame_reversal("sure option", "risky option") << "\n";
    return 0;
}
