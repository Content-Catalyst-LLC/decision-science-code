// stakeholder_legitimacy_cli.rs
// Compile with: rustc stakeholder_legitimacy_cli.rs -o stakeholder_legitimacy_cli

fn weighted_score(values: &[f64], weights: &[f64]) -> f64 {
    values.iter().zip(weights.iter()).map(|(v, w)| v * w).sum()
}

fn legitimacy_index(aggregate_score: f64, procedural_score: f64, pass_rate: f64, min_score: f64, max_burden: f64) -> f64 {
    0.40 * aggregate_score + 0.24 * procedural_score + 0.18 * pass_rate + 0.10 * min_score - 0.08 * max_burden
}

fn main() {
    let values = vec![0.68, 0.80, 0.84, 0.82, 0.86, 0.90];
    let weights = vec![0.12, 0.18, 0.28, 0.14, 0.16, 0.12];
    println!("Stakeholder score = {:.6}", weighted_score(&values, &weights));
    println!("Legitimacy index = {:.6}", legitimacy_index(0.82, 0.89, 1.0, 0.76, 0.26));
}
