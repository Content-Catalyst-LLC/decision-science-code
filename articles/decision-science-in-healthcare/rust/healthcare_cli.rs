// healthcare_cli.rs
// Compile with: rustc healthcare_cli.rs -o healthcare_cli

fn treatment_value_score(expected_benefit: f64, adverse_event_risk: f64, cost_burden: f64, patient_preference_fit: f64, equity_score: f64, implementation_feasibility: f64) -> f64 {
    0.30 * expected_benefit - 0.18 * adverse_event_risk - 0.14 * cost_burden + 0.18 * patient_preference_fit + 0.10 * equity_score + 0.10 * implementation_feasibility
}

fn queue_next(current_queue: f64, arrivals: f64, discharges: f64) -> f64 {
    (current_queue + arrivals - discharges).max(0.0)
}

fn main() {
    let score = treatment_value_score(0.72, 0.12, 0.54, 0.88, 0.76, 0.70);
    println!("Treatment value score = {:.6}", score);
    println!("Queue next = {:.6}", queue_next(18.0, 24.0, 22.0));
}
