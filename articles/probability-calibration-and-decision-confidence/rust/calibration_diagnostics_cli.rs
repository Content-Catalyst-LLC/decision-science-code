// calibration_diagnostics_cli.rs
// Compile with: rustc calibration_diagnostics_cli.rs -o calibration_diagnostics_cli

fn brier_score(probability: f64, outcome: f64) -> f64 {
    (probability - outcome).powi(2)
}

fn log_loss(probability: f64, outcome: f64) -> f64 {
    let p = probability.clamp(0.01, 0.99);
    -(outcome * p.ln() + (1.0 - outcome) * (1.0 - p).ln())
}

fn main() {
    println!("Brier score = {:.6}", brier_score(0.72, 1.0));
    println!("Log loss = {:.6}", log_loss(0.72, 1.0));
}
