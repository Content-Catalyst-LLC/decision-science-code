// future_decision_cli.rs
// Compile with: rustc future_decision_cli.rs -o future_decision_cli

fn future_maturity(ai: f64, governance: f64, uncertainty: f64, legitimacy: f64, reproducibility: f64, systems: f64, ethics: f64, adaptive: f64, failure: f64) -> f64 {
    (0.12 * ai + 0.14 * governance + 0.14 * uncertainty + 0.12 * legitimacy + 0.12 * reproducibility + 0.12 * systems + 0.14 * ethics + 0.14 * adaptive - 0.14 * failure).clamp(0.0, 1.0)
}

fn main() {
    println!("Future maturity = {:.6}", future_maturity(0.86, 0.90, 0.88, 0.84, 0.88, 0.86, 0.90, 0.88, 0.24));
}
