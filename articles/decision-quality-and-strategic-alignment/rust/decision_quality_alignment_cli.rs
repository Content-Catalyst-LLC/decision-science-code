// decision_quality_alignment_cli.rs
// Compile with: rustc decision_quality_alignment_cli.rs -o decision_quality_alignment_cli

fn weighted_score(scores: &[f64], weights: &[f64]) -> f64 {
    scores.iter().zip(weights.iter()).map(|(s, w)| s * w).sum()
}

fn main() {
    let scores = vec![0.86, 0.88, 0.82, 0.86, 0.89, 0.77];
    let weights = vec![0.16, 0.15, 0.17, 0.18, 0.18, 0.16];
    println!("Decision quality score = {:.6}", weighted_score(&scores, &weights));
}
