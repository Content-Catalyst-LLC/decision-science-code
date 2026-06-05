// decision_record_diagnostics_cli.rs
// Compile with: rustc decision_record_diagnostics_cli.rs -o decision_record_diagnostics_cli

struct Record {
    id: &'static str,
    scores: Vec<f64>,
}

fn weighted_score(scores: &[f64], weights: &[f64]) -> f64 {
    scores.iter().zip(weights).map(|(s, w)| s * w).sum()
}

fn minimum(scores: &[f64]) -> f64 {
    scores.iter().fold(f64::INFINITY, |a, &b| a.min(b))
}

fn main() {
    let weights = vec![0.10,0.09,0.11,0.11,0.12,0.10,0.09,0.10,0.09,0.09,0.10];
    let records = vec![
        Record { id: "DR-001", scores: vec![0.82,0.74,0.78,0.72,0.70,0.76,0.68,0.80,0.66,0.62,0.78] },
        Record { id: "DR-004", scores: vec![0.62,0.50,0.58,0.46,0.40,0.52,0.30,0.56,0.34,0.32,0.48] },
        Record { id: "DR-005", scores: vec![0.91,0.88,0.80,0.89,0.92,0.86,0.84,0.88,0.90,0.92,0.90] },
    ];

    for record in records {
        let quality = weighted_score(&record.scores, &weights);
        let accountable = 0.70 * quality + 0.30 * minimum(&record.scores);
        println!("{} | accountable judgment score {:.4}", record.id, accountable);
    }
}
