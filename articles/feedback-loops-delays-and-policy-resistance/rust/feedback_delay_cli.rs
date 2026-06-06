// feedback_delay_cli.rs
// Compile with: rustc feedback_delay_cli.rs -o feedback_delay_cli

fn feedback_update(state: f64, reinforcing: f64, balancing: f64, resistance: f64, disturbance: f64) -> f64 {
    state + reinforcing - balancing + resistance + disturbance
}

fn net_policy_effect(policy_delta: f64, intended_strength: f64, resistance_strength: f64, resistance_response: f64) -> f64 {
    intended_strength * policy_delta - resistance_strength * resistance_response
}

fn feedback_adjusted_score(dynamic_score: f64, average_performance: f64, worst_case: f64, threshold_pass_rate: f64) -> f64 {
    0.35 * dynamic_score + 0.25 * average_performance + 0.20 * worst_case + 0.20 * threshold_pass_rate
}

fn main() {
    println!("Next state = {:.6}", feedback_update(50.0, 4.0, 1.12, 0.4, -0.3));
    println!("Net policy effect = {:.6}", net_policy_effect(10.0, 0.8, 0.4, 6.0));
    println!("Feedback-adjusted score = {:.6}", feedback_adjusted_score(0.42, 0.79, 0.76, 1.0));
}
