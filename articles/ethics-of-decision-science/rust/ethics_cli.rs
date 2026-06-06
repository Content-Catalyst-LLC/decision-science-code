// Compile with: rustc ethics_cli.rs -o ethics_cli
fn ethical_risk(harm: f64, opacity: f64, exclusion: f64, irreversibility: f64, accountability: f64) -> f64 {
    (0.30 * harm + 0.20 * opacity + 0.22 * exclusion + 0.18 * irreversibility - 0.10 * accountability).clamp(0.0, 1.0)
}
fn legitimacy(transparency: f64, participation: f64, contestability: f64, accountability: f64) -> f64 {
    0.26 * transparency + 0.24 * participation + 0.25 * contestability + 0.25 * accountability
}
fn main() {
    println!("Ethical risk = {:.6}", ethical_risk(0.64, 0.58, 0.68, 0.56, 0.46));
    println!("Legitimacy = {:.6}", legitimacy(0.82, 0.80, 0.86, 0.90));
}
