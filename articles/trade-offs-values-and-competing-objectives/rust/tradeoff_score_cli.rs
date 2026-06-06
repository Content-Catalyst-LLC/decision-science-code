// tradeoff_score_cli.rs
// Compile with: rustc tradeoff_score_cli.rs -o tradeoff_score_cli

fn weighted_score(scores: &[f64], weights: &[f64]) -> f64 {
    scores.iter().zip(weights.iter()).map(|(s, w)| s * w).sum()
}

fn regret(score: f64, best_score: f64) -> f64 {
    best_score - score
}

fn main() {
    let scores = vec![0.90, 0.38, 0.42, 0.54, 0.48, 0.70];
    let weights = vec![0.18, 0.18, 0.20, 0.18, 0.14, 0.12];
    println!("Weighted score = {:.6}", weighted_score(&scores, &weights));
    println!("Regret = {:.6}", regret(0.72, 0.91));
}
