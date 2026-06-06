// behavioral_diagnostics_cli.rs
// Compile with: rustc behavioral_diagnostics_cli.rs -o behavioral_diagnostics_cli

fn prospect_value(x: f64, alpha: f64, beta: f64, loss_aversion: f64) -> f64 {
    if x >= 0.0 {
        x.powf(alpha)
    } else {
        -loss_aversion * (-x).powf(beta)
    }
}

fn weighted_probability(p: f64, gamma: f64) -> f64 {
    p.powf(gamma) / (p.powf(gamma) + (1.0 - p).powf(gamma)).powf(1.0 / gamma)
}

fn main() {
    println!("Gain value = {:.6}", prospect_value(100.0, 0.88, 0.88, 2.0));
    println!("Loss value = {:.6}", prospect_value(-100.0, 0.88, 0.88, 2.0));
    println!("Weighted probability = {:.6}", weighted_probability(0.10, 0.72));
}
