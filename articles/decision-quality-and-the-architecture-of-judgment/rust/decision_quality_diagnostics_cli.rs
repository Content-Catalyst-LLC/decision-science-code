// decision_quality_diagnostics_cli.rs
// Compile with: rustc decision_quality_diagnostics_cli.rs -o decision_quality_diagnostics_cli

struct Alternative {
    name: &'static str,
    scores: Vec<f64>,
}

fn weighted_score(scores: &[f64], weights: &[f64]) -> f64 {
    scores.iter().zip(weights).map(|(s, w)| s * w).sum()
}

fn main() {
    let weights = vec![0.11,0.10,0.12,0.13,0.11,0.10,0.11,0.11,0.11];
    let alternatives = vec![
        Alternative { name: "Fast Commitment", scores: vec![0.55,0.50,0.48,0.35,0.42,0.30,0.38,0.34,0.28] },
        Alternative { name: "Robust Adaptive Pathway", scores: vec![0.88,0.86,0.82,0.91,0.86,0.84,0.90,0.86,0.90] },
        Alternative { name: "Staged Learning Decision", scores: vec![0.92,0.90,0.94,0.90,0.88,0.86,0.82,0.94,0.96] },
    ];

    for alternative in alternatives {
        println!("{} | quality {:.4}", alternative.name, weighted_score(&alternative.scores, &weights));
    }
}
