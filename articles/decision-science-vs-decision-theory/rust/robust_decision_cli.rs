// robust_decision_cli.rs
// Compile with: rustc robust_decision_cli.rs -o robust_decision_cli

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
    let probabilities = vec![0.22, 0.34, 0.18, 0.16, 0.10];
    let strategies = vec![
        Strategy { name: "Optimize", payoffs: vec![145.0, 92.0, 30.0, -95.0, -40.0] },
        Strategy { name: "Robust", payoffs: vec![78.0, 72.0, 65.0, 48.0, 55.0] },
        Strategy { name: "Adaptive", payoffs: vec![98.0, 80.0, 62.0, 38.0, 68.0] },
    ];

    for strategy in strategies {
        println!(
            "{} | EV {:.3} | robustness {:.3}",
            strategy.name,
            expected_value(&strategy.payoffs, &probabilities),
            robustness(&strategy.payoffs, 45.0)
        );
    }
}
