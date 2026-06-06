// value_of_information_cli.rs
// Compile with: rustc value_of_information_cli.rs -o value_of_information_cli

fn expected_value(values: &[f64], probabilities: &[f64]) -> f64 {
    values.iter().zip(probabilities.iter()).map(|(v, p)| v * p).sum()
}

fn evpi(perfect_information_value: f64, current_expected_value: f64) -> f64 {
    perfect_information_value - current_expected_value
}

fn net_value_waiting(evsi: f64, information_cost: f64, delay_cost: f64) -> f64 {
    evsi - information_cost - delay_cost
}

fn main() {
    let values = vec![82.0, 28.0, 40.0, 76.0];
    let probabilities = vec![0.35, 0.25, 0.20, 0.20];

    println!("Expected value = {:.6}", expected_value(&values, &probabilities));
    println!("EVPI = {:.6}", evpi(76.4, 68.1));
    println!("Net value waiting = {:.6}", net_value_waiting(4.4, 2.0, 1.3));
}
