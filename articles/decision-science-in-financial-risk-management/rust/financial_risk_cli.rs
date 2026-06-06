// financial_risk_cli.rs
// Compile with: rustc financial_risk_cli.rs -o financial_risk_cli

fn expected_loss(losses: &[f64], probabilities: &[f64]) -> f64 {
    losses.iter().zip(probabilities.iter()).map(|(l, p)| l * p).sum()
}

fn capital_next(current_capital: f64, period_return_pct: f64, floor: f64) -> f64 {
    (current_capital * (1.0 + period_return_pct / 100.0)).max(floor)
}

fn main() {
    let losses = [-1.2, -4.8, -3.6, -6.2];
    let probs = [0.55, 0.20, 0.15, 0.10];
    println!("Expected loss = {:.6}", expected_loss(&losses, &probs));
    println!("Capital next = {:.6}", capital_next(100.0, -8.5, 20.0));
}
