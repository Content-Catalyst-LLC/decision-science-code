// regret_minimax_cli.rs
// Compile with: rustc regret_minimax_cli.rs -o regret_minimax_cli

fn expected_value(values: &[f64], weights: &[f64]) -> f64 {
    values.iter().zip(weights.iter()).map(|(v, w)| v * w).sum()
}

fn maximin_value(values: &[f64]) -> f64 {
    values.iter().copied().fold(f64::INFINITY, f64::min)
}

fn maximum_regret(regrets: &[f64]) -> f64 {
    regrets.iter().copied().fold(f64::NEG_INFINITY, f64::max)
}

fn main() {
    let values = vec![0.73, 0.81, 0.79, 0.87, 0.76, 0.77];
    let weights = vec![0.18, 0.16, 0.18, 0.17, 0.15, 0.16];
    let regrets = vec![0.19, 0.00, 0.05, 0.01, 0.06, 0.06];

    println!("Expected value = {:.6}", expected_value(&values, &weights));
    println!("Maximin value = {:.6}", maximin_value(&values));
    println!("Maximum regret = {:.6}", maximum_regret(&regrets));
}
