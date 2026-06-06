// complex_system_decision_cli.rs
// Compile with: rustc complex_system_decision_cli.rs -o complex_system_decision_cli

fn complex_system_score(adaptability: f64, robustness: f64, feedback: f64, interdependence: f64, burden: f64, legitimacy: f64, threshold_resilience: f64) -> f64 {
    0.18 * adaptability + 0.18 * robustness + 0.16 * feedback + 0.16 * interdependence - 0.10 * burden + 0.12 * legitimacy + 0.20 * threshold_resilience
}

fn feedback_update(state: f64, reinforcing: f64, balancing: f64, disturbance: f64) -> f64 {
    state + reinforcing - balancing + disturbance
}

fn main() {
    println!("Complex-system score = {:.6}", complex_system_score(0.81, 0.86, 0.82, 0.83, 0.44, 0.78, 0.86));
    println!("Next state = {:.6}", feedback_update(52.0, 3.0, 1.4, -0.2));
}
