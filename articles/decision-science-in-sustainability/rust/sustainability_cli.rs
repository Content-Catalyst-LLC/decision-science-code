// sustainability_cli.rs
// Compile with: rustc sustainability_cli.rs -o sustainability_cli

fn sustainability_value_score(emissions_reduction: f64, social_equity: f64, cost_burden: f64, resilience_score: f64, implementation_feasibility: f64, threshold_protection: f64) -> f64 {
    0.22 * emissions_reduction + 0.20 * social_equity - 0.12 * cost_burden + 0.18 * resilience_score + 0.12 * implementation_feasibility + 0.16 * threshold_protection
}

fn threshold_breach(resource_stock: f64, threshold: f64) -> bool {
    resource_stock < threshold
}

fn main() {
    let score = sustainability_value_score(0.61, 0.74, 0.49, 0.82, 0.66, 0.82);
    println!("Sustainability value score = {:.6}", score);
    println!("Threshold breach? {}", threshold_breach(34.0, 35.0));
}
