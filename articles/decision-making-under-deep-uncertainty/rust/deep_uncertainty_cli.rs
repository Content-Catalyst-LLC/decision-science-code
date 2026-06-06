// deep_uncertainty_cli.rs
// Compile with: rustc deep_uncertainty_cli.rs -o deep_uncertainty_cli

fn expected_value(values: &[f64], weights: &[f64]) -> f64 {
    values.iter().zip(weights.iter()).map(|(v, w)| v * w).sum()
}

fn worst_case(values: &[f64]) -> f64 {
    values.iter().copied().fold(f64::INFINITY, f64::min)
}

fn threshold_pass_rate(values: &[f64], threshold: f64) -> f64 {
    let passed = values.iter().filter(|v| **v >= threshold).count();
    passed as f64 / values.len() as f64
}

fn main() {
    let values = vec![0.72, 0.80, 0.78, 0.87, 0.75, 0.77];
    let weights = vec![0.1666666667; 6];
    println!("Expected value = {:.6}", expected_value(&values, &weights));
    println!("Worst case = {:.6}", worst_case(&values));
    println!("Pass rate = {:.6}", threshold_pass_rate(&values, 0.70));
}
