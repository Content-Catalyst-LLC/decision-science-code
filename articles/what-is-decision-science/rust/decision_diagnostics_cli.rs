// decision_diagnostics_cli.rs
// Compile with: rustc decision_diagnostics_cli.rs -o decision_diagnostics_cli

#[derive(Debug)]
struct Alternative {
    name: &'static str,
    payoffs: Vec<f64>,
}

fn expected_value(payoffs: &[f64], probabilities: &[f64]) -> f64 {
    payoffs.iter().zip(probabilities.iter()).map(|(x, p)| x * p).sum()
}

fn robustness_share(payoffs: &[f64], threshold: f64) -> f64 {
    let count = payoffs.iter().filter(|x| **x >= threshold).count();
    count as f64 / payoffs.len() as f64
}

fn main() {
    let probabilities = vec![0.40, 0.35, 0.25];
    let alternatives = vec![
        Alternative { name: "Optimize", payoffs: vec![120.0, 25.0, -80.0] },
        Alternative { name: "Hedge", payoffs: vec![90.0, 62.0, 12.0] },
        Alternative { name: "Preserve Option", payoffs: vec![66.0, 58.0, 42.0] },
    ];

    for alt in alternatives {
        let ev = expected_value(&alt.payoffs, &probabilities);
        let robust = robustness_share(&alt.payoffs, 35.0);
        println!("{} | expected value: {:.3} | robustness: {:.3}", alt.name, ev, robust);
    }
}
