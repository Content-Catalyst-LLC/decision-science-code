// judgment_diagnostics_cli.rs
// Compile with: rustc judgment_diagnostics_cli.rs -o judgment_diagnostics_cli

fn posterior_from_likelihoods(prior: f64, likelihood_true: f64, likelihood_false: f64) -> f64 {
    let odds = prior / (1.0 - prior);
    let posterior_odds = odds * (likelihood_true / likelihood_false);
    posterior_odds / (1.0 + posterior_odds)
}

fn brier_score(probability: f64, outcome: f64) -> f64 {
    (probability - outcome).powi(2)
}

fn main() {
    println!("Posterior = {:.6}", posterior_from_likelihoods(0.35, 0.72, 0.28));
    println!("Brier score = {:.6}", brier_score(0.62, 1.0));
}
