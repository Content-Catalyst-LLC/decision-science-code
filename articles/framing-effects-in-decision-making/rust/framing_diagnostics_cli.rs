// framing_diagnostics_cli.rs
// Compile with: rustc framing_diagnostics_cli.rs -o framing_diagnostics_cli

fn prospect_value(x: f64, alpha: f64, beta: f64, loss_aversion: f64) -> f64 {
    if x >= 0.0 {
        x.powf(alpha)
    } else {
        -loss_aversion * (-x).powf(beta)
    }
}

fn main() {
    println!("Gain value = {:.6}", prospect_value(100.0, 0.88, 0.88, 2.0));
    println!("Loss value = {:.6}", prospect_value(-100.0, 0.88, 0.88, 2.0));
}
