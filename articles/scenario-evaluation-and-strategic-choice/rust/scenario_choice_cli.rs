// scenario_choice_cli.rs
// Compile with: rustc scenario_choice_cli.rs -o scenario_choice_cli

fn expected_value(values: &[f64], probabilities: &[f64]) -> f64 {
    values.iter().zip(probabilities.iter()).map(|(v, p)| v * p).sum()
}

fn worst_case(values: &[f64]) -> f64 {
    values.iter().fold(f64::INFINITY, |a, &b| a.min(b))
}

fn threshold_pass_rate(values: &[f64], threshold: f64) -> f64 {
    let count = values.iter().filter(|&&v| v >= threshold).count();
    count as f64 / values.len() as f64
}

fn main() {
    let values = [0.78, 0.76, 0.82, 0.80, 0.81];
    let probabilities = [0.22, 0.24, 0.20, 0.18, 0.16];
    println!("Expected value = {:.6}", expected_value(&values, &probabilities));
    println!("Worst case = {:.6}", worst_case(&values));
    println!("Threshold pass rate = {:.6}", threshold_pass_rate(&values, 0.70));
}
