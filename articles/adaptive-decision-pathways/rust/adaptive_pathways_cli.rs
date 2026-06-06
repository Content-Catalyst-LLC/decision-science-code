// adaptive_pathways_cli.rs
// Compile with: rustc adaptive_pathways_cli.rs -o adaptive_pathways_cli

fn pathway_score(initial_performance: f64, flexibility: f64, monitoring_quality: f64, trigger_clarity: f64, switching_cost: f64, fallback_strength: f64) -> f64 {
    0.20 * initial_performance + 0.18 * flexibility + 0.16 * monitoring_quality + 0.16 * trigger_clarity - 0.12 * switching_cost + 0.18 * fallback_strength
}

fn trigger_hit(system_stress: f64, option_value: f64, stress_trigger: f64, option_value_trigger: f64) -> bool {
    system_stress >= stress_trigger || option_value <= option_value_trigger
}

fn main() {
    let score = pathway_score(0.76, 0.88, 0.82, 0.80, 0.38, 0.84);
    println!("Pathway score = {:.6}", score);
    println!("Trigger hit? {}", trigger_hit(0.70, 0.55, 0.68, 0.40));
}
