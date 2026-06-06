// mcda_score_cli.rs
// Compile with: rustc mcda_score_cli.rs -o mcda_score_cli

fn weighted_score(scores: &[f64], weights: &[f64]) -> f64 {
    scores.iter().zip(weights.iter()).map(|(s, w)| s * w).sum()
}

fn main() {
    let scores = vec![0.8, 0.6, 0.9];
    let weights = vec![0.3, 0.3, 0.4];
    println!("Weighted score = {:.6}", weighted_score(&scores, &weights));
}
