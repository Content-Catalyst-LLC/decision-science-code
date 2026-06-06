// group_influence_diagnostics_cli.rs
// Compile with: rustc group_influence_diagnostics_cli.rs -o group_influence_diagnostics_cli

fn collective_error(group_estimate: f64, true_value: f64) -> f64 {
    (group_estimate - true_value).abs()
}

fn hidden_profile_risk(shared_information: f64, unique_information: f64) -> f64 {
    unique_information / (shared_information + unique_information)
}

fn main() {
    println!("Collective error = {:.6}", collective_error(0.64, 0.62));
    println!("Hidden-profile risk = {:.6}", hidden_profile_risk(5.0, 9.0));
}
