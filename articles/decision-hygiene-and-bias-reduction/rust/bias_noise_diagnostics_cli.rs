// bias_noise_diagnostics_cli.rs
// Compile with: rustc bias_noise_diagnostics_cli.rs -o bias_noise_diagnostics_cli

fn bias(errors: &[f64]) -> f64 {
    errors.iter().sum::<f64>() / errors.len() as f64
}

fn mse(errors: &[f64]) -> f64 {
    errors.iter().map(|e| e * e).sum::<f64>() / errors.len() as f64
}

fn brier_score(probability: f64, outcome: f64) -> f64 {
    (probability - outcome).powi(2)
}

fn main() {
    let errors = vec![0.12, 0.04, -0.03, 0.08];
    println!("Bias = {:.6}", bias(&errors));
    println!("MSE = {:.6}", mse(&errors));
    println!("Brier score = {:.6}", brier_score(0.69, 0.0));
}
