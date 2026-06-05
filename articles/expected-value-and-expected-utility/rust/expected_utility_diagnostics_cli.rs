// expected_utility_diagnostics_cli.rs
// Compile with: rustc expected_utility_diagnostics_cli.rs -o expected_utility_diagnostics_cli

fn expected_value(outcomes: &[f64], probabilities: &[f64]) -> f64 {
    outcomes.iter().zip(probabilities).map(|(x, p)| x * p).sum()
}

fn crra(x: f64, rho: f64, offset: f64) -> f64 {
    let z = x + offset;
    if (rho - 1.0).abs() < 1e-9 {
        z.ln()
    } else {
        (z.powf(1.0 - rho) - 1.0) / (1.0 - rho)
    }
}

fn expected_utility(outcomes: &[f64], probabilities: &[f64], rho: f64) -> f64 {
    outcomes.iter().zip(probabilities).map(|(x, p)| p * crra(*x, rho, 151.0)).sum()
}

fn main() {
    let outcomes = vec![180.0, 40.0];
    let probabilities = vec![0.60, 0.40];

    println!("EV = {:.4}", expected_value(&outcomes, &probabilities));
    println!("EU rho=1 = {:.6}", expected_utility(&outcomes, &probabilities, 1.0));
}
