// ai_governance_cli.rs
// Compile with: rustc ai_governance_cli.rs -o ai_governance_cli

fn composite_ai_risk(safety: f64, equity: f64, bias: f64, privacy: f64, opacity: f64, security: f64) -> f64 {
    0.20 * safety + 0.18 * equity + 0.16 * bias + 0.16 * privacy + 0.14 * opacity + 0.16 * security
}

fn drift_indicator(current_metric: f64, baseline_metric: f64) -> f64 {
    (current_metric - baseline_metric).abs()
}

fn main() {
    println!("Composite AI risk = {:.6}", composite_ai_risk(0.52, 0.48, 0.50, 0.42, 0.55, 0.46));
    println!("Drift indicator = {:.6}", drift_indicator(0.77, 0.86));
}
