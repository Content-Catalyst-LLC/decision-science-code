// systems_modeling_cli.rs
// Compile with: rustc systems_modeling_cli.rs -o systems_modeling_cli

fn stock_update(stock: f64, inflow: f64, outflow: f64) -> f64 {
    stock + inflow - outflow
}

fn feedback_update(state: f64, reinforcing: f64, balancing: f64, disturbance: f64) -> f64 {
    state + reinforcing - balancing + disturbance
}

fn systems_decision_score(dynamic_score: f64, average_performance: f64, worst_case: f64, threshold_pass_rate: f64) -> f64 {
    0.35 * dynamic_score + 0.25 * average_performance + 0.20 * worst_case + 0.20 * threshold_pass_rate
}

fn main() {
    println!("Next stock = {:.6}", stock_update(100.0, 12.0, 8.5));
    println!("Next state = {:.6}", feedback_update(55.0, 3.85, 2.10, -0.4));
    println!("Systems decision score = {:.6}", systems_decision_score(0.78, 0.82, 0.79, 1.0));
}
