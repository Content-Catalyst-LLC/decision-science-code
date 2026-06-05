// bayesian_diagnostics_cli.rs
// Compile with: rustc bayesian_diagnostics_cli.rs -o bayesian_diagnostics_cli

fn bayesian_update(prior: f64, sensitivity: f64, false_positive_rate: f64) -> f64 {
    let numerator = sensitivity * prior;
    let denominator = numerator + false_positive_rate * (1.0 - prior);
    numerator / denominator
}

fn posterior_expected_utility(posterior: f64, utility_true: f64, utility_false: f64) -> f64 {
    posterior * utility_true + (1.0 - posterior) * utility_false
}

fn main() {
    let posterior = bayesian_update(0.10, 0.86, 0.12);
    let act = posterior_expected_utility(posterior, 90.0, -25.0);
    let wait = posterior_expected_utility(posterior, -80.0, 15.0);

    println!("Posterior = {:.6}", posterior);
    println!("Action utility = {:.6}", act);
    println!("Wait utility = {:.6}", wait);
}
