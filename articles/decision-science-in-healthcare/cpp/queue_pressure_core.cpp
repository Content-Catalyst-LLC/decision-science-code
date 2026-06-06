// queue_pressure_core.cpp
// Compile with: g++ -std=c++17 queue_pressure_core.cpp -o queue_pressure_core

#include <algorithm>
#include <iostream>

double queue_next(double current_queue, double arrivals, double discharges) {
    return std::max(0.0, current_queue + arrivals - discharges);
}

double queue_pressure(double queue, double reference_capacity) {
    return std::min(1.0, queue / reference_capacity);
}

int main() {
    double q = queue_next(18.0, 24.0, 22.0);
    std::cout << "Queue next = " << q << "\n";
    std::cout << "Queue pressure = " << queue_pressure(q, 60.0) << "\n";
    return 0;
}
