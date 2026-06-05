// core_principles_diagnostics_cli.rs
// Compile with: rustc core_principles_diagnostics_cli.rs -o core_principles_diagnostics_cli

struct Alternative {
    name: &'static str,
    scores: Vec<f64>,
}

fn weighted_score(scores: &[f64], weights: &[f64]) -> f64 {
    scores.iter().zip(weights).map(|(s, w)| s * w).sum()
}

fn main() {
    let weights = vec![0.12, 0.14, 0.12, 0.10, 0.11, 0.14, 0.12, 0.08, 0.07];
    let alternatives = vec![
        Alternative { name: "Fast Expansion", scores: vec![0.55,0.42,0.40,0.36,0.44,0.38,0.44,0.52,0.30] },
        Alternative { name: "Adaptive Learning Strategy", scores: vec![0.88,0.87,0.85,0.84,0.86,0.86,0.93,0.84,0.88] },
        Alternative { name: "Evidence-First Pilot", scores: vec![0.92,0.90,0.91,0.88,0.80,0.78,0.89,0.94,0.95] },
    ];

    for alternative in alternatives {
        println!("{} | score {:.4}", alternative.name, weighted_score(&alternative.scores, &weights));
    }
}
