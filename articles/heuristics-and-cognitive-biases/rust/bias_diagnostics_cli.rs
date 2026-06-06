// bias_diagnostics_cli.rs
// Compile with: rustc bias_diagnostics_cli.rs -o bias_diagnostics_cli

fn anchored_estimate(anchor: f64, evidence: f64, weight: f64) -> f64 {
    weight * anchor + (1.0 - weight) * evidence
}

fn brier_score(probability: f64, outcome: f64) -> f64 {
    (probability - outcome).powi(2)
}

fn main() {
    println!("Anchored estimate = {:.6}", anchored_estimate(0.80, 0.42, 0.45));
    println!("Brier score = {:.6}", brier_score(0.72, 1.0));
}
