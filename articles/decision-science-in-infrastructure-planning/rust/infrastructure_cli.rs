// infrastructure_cli.rs
// Compile with: rustc infrastructure_cli.rs -o infrastructure_cli

fn expected_value(values: &[f64], probabilities: &[f64]) -> f64 {
    values.iter().zip(probabilities.iter()).map(|(v, p)| v * p).sum()
}

fn trigger_reached(indicator: f64, threshold: f64) -> bool {
    indicator >= threshold
}

fn main() {
    let values = [76.0, 76.0, 82.0, 70.0, 78.0];
    let probabilities = [0.30, 0.20, 0.20, 0.15, 0.15];
    println!("Expected service value = {:.6}", expected_value(&values, &probabilities));
    println!("Adaptive trigger reached = {}", trigger_reached(0.74, 0.70));
}
