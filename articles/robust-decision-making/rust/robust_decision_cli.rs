fn expected_value(values: &[f64], weights: &[f64]) -> f64 { values.iter().zip(weights.iter()).map(|(v, w)| v * w).sum() }
fn worst_case(values: &[f64]) -> f64 { values.iter().copied().fold(f64::INFINITY, f64::min) }
fn threshold_pass_rate(values: &[f64], threshold: f64) -> f64 { values.iter().filter(|v| **v >= threshold).count() as f64 / values.len() as f64 }
fn main() {
    let values = vec![0.73, 0.77, 0.79, 0.81, 0.76, 0.86];
    let weights = vec![0.18, 0.17, 0.18, 0.16, 0.15, 0.16];
    println!("Expected value = {:.6}", expected_value(&values, &weights));
    println!("Worst case = {:.6}", worst_case(&values));
    println!("Pass rate = {:.6}", threshold_pass_rate(&values, 0.70));
}
