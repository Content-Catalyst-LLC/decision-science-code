// democratic_reasoning_cli.rs
// Compile with: rustc democratic_reasoning_cli.rs -o democratic_reasoning_cli

fn legitimacy_score(transparency: f64, participation: f64, fairness: f64, evidence: f64, contestability: f64, accountability: f64) -> f64 {
    0.17 * transparency + 0.17 * participation + 0.18 * fairness + 0.16 * evidence + 0.16 * contestability + 0.16 * accountability
}

fn next_trust(current: f64, performance: f64, transparency: f64, responsiveness: f64, fairness: f64, uncertainty: f64, harm: f64) -> f64 {
    (current + 0.08 * performance + 0.06 * transparency + 0.08 * responsiveness + 0.08 * fairness - 0.06 * uncertainty - 0.10 * harm).clamp(0.0, 1.0)
}

fn main() {
    println!("Legitimacy score = {:.6}", legitimacy_score(0.88, 0.88, 0.88, 0.84, 0.86, 0.88));
    println!("Next trust = {:.6}", next_trust(0.62, 0.70, 0.78, 0.74, 0.72, 0.36, 0.30));
}
