// decision_tree_diagnostics_cli.rs
// Compile with: rustc decision_tree_diagnostics_cli.rs -o decision_tree_diagnostics_cli

fn expected_value(success_payoff: f64, failure_payoff: f64, success_probability: f64, cost: f64, credit: f64) -> f64 {
    success_payoff * success_probability + failure_payoff * (1.0 - success_probability) - cost + credit
}

fn main() {
    let immediate = expected_value(125.0, -35.0, 0.58, 0.0, 0.0);
    let staged = expected_value(145.0, -20.0, 0.54, 12.0, 18.0);

    println!("Immediate EV = {:.4}", immediate);
    println!("Staged EV = {:.4}", staged);
    println!("Net value of staging = {:.4}", staged - immediate);
}
