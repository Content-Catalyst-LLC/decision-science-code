// organizational_strategy_cli.rs
// Compile with: rustc organizational_strategy_cli.rs -o organizational_strategy_cli

fn expected_value(values: &[f64], probabilities: &[f64]) -> f64 {
    values.iter().zip(probabilities.iter()).map(|(v, p)| v * p).sum()
}

fn robust_strategy_score(expected_value: f64, downside_robustness: f64, adaptability: f64, reversibility: f64) -> f64 {
    0.36 * expected_value / 100.0 + 0.30 * downside_robustness / 100.0 + 0.20 * adaptability + 0.14 * reversibility
}

fn main() {
    let values = [68.0, 82.0, 89.0, 66.0];
    let probabilities = [0.25, 0.35, 0.20, 0.20];
    let ev = expected_value(&values, &probabilities);
    println!("Expected strategic value = {:.6}", ev);
    println!("Robust strategy score = {:.6}", robust_strategy_score(ev, 66.0, 0.84, 0.82));
}
