// historical_decision_diagnostics_cli.rs
// Compile with: rustc historical_decision_diagnostics_cli.rs -o historical_decision_diagnostics_cli

struct Strategy {
    name: &'static str,
    payoffs: Vec<f64>,
}

fn expected_value(payoffs: &[f64], probabilities: &[f64]) -> f64 {
    payoffs.iter().zip(probabilities).map(|(x, p)| x * p).sum()
}

fn robustness(payoffs: &[f64], threshold: f64) -> f64 {
    payoffs.iter().filter(|x| **x >= threshold).count() as f64 / payoffs.len() as f64
}

fn main() {
    let probabilities = vec![0.42, 0.28, 0.18, 0.12];
    let strategies = vec![
        Strategy { name: "Aggressive", payoffs: vec![128.0, 50.0, -90.0, -20.0] },
        Strategy { name: "Balanced", payoffs: vec![92.0, 68.0, 18.0, 42.0] },
        Strategy { name: "Defensive", payoffs: vec![62.0, 58.0, 44.0, 54.0] },
        Strategy { name: "Adaptive", payoffs: vec![88.0, 70.0, 36.0, 72.0] },
    ];

    for strategy in strategies {
        println!(
            "{} | EV {:.3} | robustness {:.3}",
            strategy.name,
            expected_value(&strategy.payoffs, &probabilities),
            robustness(&strategy.payoffs, 40.0)
        );
    }
}
