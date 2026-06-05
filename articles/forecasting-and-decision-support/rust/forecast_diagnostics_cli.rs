// forecast_diagnostics_cli.rs
// Compile with: rustc forecast_diagnostics_cli.rs -o forecast_diagnostics_cli

fn brier_score(probability: f64, outcome: f64) -> f64 {
    (probability - outcome).powi(2)
}

fn threshold_from_costs(false_positive_cost: f64, false_negative_cost: f64) -> f64 {
    false_positive_cost / (false_positive_cost + false_negative_cost)
}

fn main() {
    println!("Brier score = {:.6}", brier_score(0.62, 1.0));
    println!("Decision threshold = {:.6}", threshold_from_costs(15.0, 85.0));
}
