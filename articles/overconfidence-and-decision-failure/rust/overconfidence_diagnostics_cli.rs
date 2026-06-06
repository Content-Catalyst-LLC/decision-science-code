// overconfidence_diagnostics_cli.rs
// Compile with: rustc overconfidence_diagnostics_cli.rs -o overconfidence_diagnostics_cli

fn brier_score(probability: f64, outcome: f64) -> f64 {
    (probability - outcome).powi(2)
}

fn confidence_error(confidence: f64, accuracy_proxy: f64) -> f64 {
    confidence - accuracy_proxy
}

fn planning_error(actual: f64, estimate: f64) -> f64 {
    (actual - estimate) / estimate
}

fn main() {
    println!("Brier score = {:.6}", brier_score(0.69, 0.0));
    println!("Confidence error = {:.6}", confidence_error(0.88, 0.52));
    println!("Planning error = {:.6}", planning_error(520.0, 365.0));
}
