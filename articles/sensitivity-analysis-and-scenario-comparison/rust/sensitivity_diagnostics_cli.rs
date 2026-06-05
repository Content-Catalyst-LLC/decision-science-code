// sensitivity_diagnostics_cli.rs
// Compile with: rustc sensitivity_diagnostics_cli.rs -o sensitivity_diagnostics_cli

fn strategy_score(
    base: f64,
    demand_sensitivity: f64,
    cost_sensitivity: f64,
    disruption_sensitivity: f64,
    resilience_buffer: f64,
    adaptation_capacity: f64,
    demand: f64,
    cost: f64,
    disruption: f64,
) -> f64 {
    base
        + demand_sensitivity * demand
        - cost_sensitivity * cost
        - disruption_sensitivity * disruption
        + resilience_buffer * disruption.max(0.0)
        + adaptation_capacity * demand.abs()
}

fn main() {
    let balanced = strategy_score(75.0, 8.0, 10.0, 11.0, 9.0, 7.0, 0.5, 0.3, 0.2);
    let adaptive = strategy_score(73.0, 7.0, 9.0, 9.0, 12.0, 12.0, 0.5, 0.3, 0.2);

    println!("Balanced score = {:.4}", balanced);
    println!("Adaptive score = {:.4}", adaptive);
}
