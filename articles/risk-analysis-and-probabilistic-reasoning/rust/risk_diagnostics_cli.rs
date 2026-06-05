// risk_diagnostics_cli.rs
// Compile with: rustc risk_diagnostics_cli.rs -o risk_diagnostics_cli

fn expected_loss(probabilities: &[f64], losses: &[f64]) -> f64 {
    probabilities.iter().zip(losses).map(|(p, l)| p * l).sum()
}

fn bayesian_update(prior: f64, sensitivity: f64, false_positive_rate: f64) -> f64 {
    let evidence_probability = sensitivity * prior + false_positive_rate * (1.0 - prior);
    (sensitivity * prior) / evidence_probability
}

fn main() {
    let probabilities = vec![0.08, 0.06, 0.03];
    let losses = vec![0.035, 0.040, 0.075];

    println!("Expected loss = {:.6}", expected_loss(&probabilities, &losses));
    println!("Posterior risk = {:.6}", bayesian_update(0.10, 0.82, 0.12));
}
