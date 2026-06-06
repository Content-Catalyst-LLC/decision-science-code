// path_dependence_cli.rs
// Compile with: rustc path_dependence_cli.rs -o path_dependence_cli

fn switching_cost(investment: f64, network_dependence: f64, institutional_routine: f64) -> f64 {
    0.36 * investment + 0.34 * network_dependence + 0.30 * institutional_routine
}

fn lock_in_risk(switching_cost: f64, institutional_routine: f64, network_dependence: f64, option_value: f64) -> f64 {
    0.42 * switching_cost + 0.28 * institutional_routine + 0.20 * network_dependence - 0.10 * option_value
}

fn should_review(lock_in_risk: f64, option_value: f64, lock_in_threshold: f64, option_threshold: f64) -> bool {
    lock_in_risk >= lock_in_threshold || option_value <= option_threshold
}

fn main() {
    let cost = switching_cost(0.55, 0.62, 0.58);
    let risk = lock_in_risk(cost, 0.62, 0.55, 0.40);
    println!("Switching cost = {:.6}", cost);
    println!("Lock-in risk = {:.6}", risk);
    println!("Review? {}", should_review(risk, 0.40, 0.72, 0.35));
}
