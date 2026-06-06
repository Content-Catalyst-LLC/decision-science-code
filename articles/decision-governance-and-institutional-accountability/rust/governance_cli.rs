// governance_cli.rs
// Compile with: rustc governance_cli.rs -o governance_cli

fn accountability_score(decision_rights: f64, traceability: f64, review: f64, ownership: f64, monitoring: f64, corrective: f64) -> f64 {
    0.18 * decision_rights + 0.17 * traceability + 0.18 * review + 0.17 * ownership + 0.15 * monitoring + 0.15 * corrective
}

fn responsibility_gap(influence: f64, accountability: f64) -> f64 {
    (influence - accountability).max(0.0)
}

fn main() {
    println!("Accountability score = {:.6}", accountability_score(0.82, 0.86, 0.88, 0.84, 0.90, 0.92));
    println!("Responsibility gap = {:.6}", responsibility_gap(0.62, 0.34));
}
