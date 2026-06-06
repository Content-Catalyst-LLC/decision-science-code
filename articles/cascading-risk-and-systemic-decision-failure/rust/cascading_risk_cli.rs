// cascading_risk_cli.rs
// Compile with: rustc cascading_risk_cli.rs -o cascading_risk_cli

fn cascade_risk_score(exposure: f64, dependency_centrality: f64, buffer_weakness: f64, common_mode_risk: f64, monitoring_quality: f64, response_capacity: f64) -> f64 {
    0.22 * exposure + 0.22 * dependency_centrality + 0.20 * buffer_weakness + 0.18 * common_mode_risk - 0.09 * monitoring_quality - 0.09 * response_capacity
}

fn threshold_failure(stress: f64, neighbor_failure_load: f64, buffer: f64, threshold: f64) -> bool {
    let effective_stress = stress + neighbor_failure_load + (0.40 - buffer).max(0.0);
    effective_stress >= threshold
}

fn main() {
    let score = cascade_risk_score(0.82, 0.88, 0.76, 0.79, 0.42, 0.40);
    println!("Cascade risk score = {:.6}", score);
    println!("Threshold failure? {}", threshold_failure(0.52, 0.18, 0.31, 0.66));
}
