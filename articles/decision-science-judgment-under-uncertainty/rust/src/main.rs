fn expected_value(outcomes: &[(f64, f64)]) -> f64 {
    outcomes.iter().map(|(probability, value)| probability * value).sum()
}

fn main() {
    let outcomes = vec![(0.65, 72.0), (0.35, 38.0)];

    println!("Decision Science CLI");
    println!("Expected value: {:.3}", expected_value(&outcomes));
    println!("Interpretation: expected value supports judgment; it does not replace it.");
}
