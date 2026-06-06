// resilience_long_horizon_cli.rs
// Compile with: rustc resilience_long_horizon_cli.rs -o resilience_long_horizon_cli

fn resilience_update(current: f64, recovery: f64, investment: f64, degradation: f64, shock: f64) -> f64 {
    (current + recovery + investment - degradation - shock).max(0.0)
}

fn resilient_decision_score(long_horizon_score: f64, average_performance: f64, worst_case: f64, pass_rate: f64, performance_range: f64) -> f64 {
    0.30 * long_horizon_score + 0.24 * average_performance + 0.22 * worst_case + 0.18 * pass_rate - 0.06 * performance_range
}

fn should_revise(system_state: f64, resilience_capacity: f64, stress_threshold: f64, resilience_threshold: f64) -> bool {
    system_state >= stress_threshold || resilience_capacity <= resilience_threshold
}

fn main() {
    println!("Next resilience stock = {:.6}", resilience_update(35.0, 3.0, 2.0, 1.0, 1.6));
    println!("Resilient decision score = {:.6}", resilient_decision_score(0.80, 0.79, 0.74, 1.0, 0.10));
    println!("Revise? {}", should_revise(72.0, 24.0, 80.0, 25.0));
}
