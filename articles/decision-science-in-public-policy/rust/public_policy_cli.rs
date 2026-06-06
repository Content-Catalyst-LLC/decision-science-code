// public_policy_cli.rs
// Compile with: rustc public_policy_cli.rs -o public_policy_cli

fn policy_value_score(efficiency: f64, equity: f64, resilience: f64, feasibility: f64, legitimacy: f64, implementation_capacity: f64) -> f64 {
    0.18 * efficiency + 0.22 * equity + 0.18 * resilience + 0.14 * feasibility + 0.14 * legitimacy + 0.14 * implementation_capacity
}

fn requires_review(equity: f64, legitimacy: f64, implementation_capacity: f64) -> bool {
    equity < 0.55 || legitimacy < 0.55 || implementation_capacity < 0.55
}

fn main() {
    let score = policy_value_score(0.72, 0.84, 0.70, 0.76, 0.80, 0.86);
    println!("Policy value score = {:.6}", score);
    println!("Requires review? {}", requires_review(0.46, 0.54, 0.68));
}
