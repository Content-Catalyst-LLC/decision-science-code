// uncertainty_diagnostics_cli.rs
// Compile with: rustc uncertainty_diagnostics_cli.rs -o uncertainty_diagnostics_cli

struct Strategy {
    name: &'static str,
    payoffs: Vec<f64>,
    ambiguity: f64,
}

fn expected_value(payoffs: &[f64], probabilities: &[f64]) -> f64 {
    payoffs.iter().zip(probabilities).map(|(x, p)| x * p).sum()
}

fn robustness(payoffs: &[f64], threshold: f64) -> f64 {
    payoffs.iter().filter(|x| **x >= threshold).count() as f64 / payoffs.len() as f64
}

fn main() {
    let probabilities = vec![0.40, 0.24, 0.16, 0.10, 0.10];
    let strategies = vec![
        Strategy { name: "Expand", payoffs: vec![120.0, 45.0, -95.0, -130.0, 20.0], ambiguity: 0.42 },
        Strategy { name: "Hedge", payoffs: vec![92.0, 68.0, 18.0, -20.0, 55.0], ambiguity: 0.22 },
        Strategy { name: "Preserve Option", payoffs: vec![72.0, 62.0, 42.0, 18.0, 70.0], ambiguity: 0.08 },
        Strategy { name: "Adaptive Pathway", payoffs: vec![95.0, 72.0, 34.0, 10.0, 78.0], ambiguity: 0.15 },
    ];

    for strategy in strategies {
        println!(
            "{} | EV {:.3} | robustness {:.3} | ambiguity {:.3}",
            strategy.name,
            expected_value(&strategy.payoffs, &probabilities),
            robustness(&strategy.payoffs, 40.0),
            strategy.ambiguity
        );
    }
}
