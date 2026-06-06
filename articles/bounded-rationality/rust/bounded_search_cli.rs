// bounded_search_cli.rs
// Compile with: rustc bounded_search_cli.rs -o bounded_search_cli

fn first_satisficing(values: &[f64], aspiration: f64) -> Option<(usize, f64)> {
    for (index, value) in values.iter().enumerate() {
        if *value >= aspiration {
            return Some((index + 1, *value));
        }
    }
    None
}

fn main() {
    let values = vec![0.58, 0.71, 0.82, 0.77, 0.91];
    let aspiration = 0.75;

    match first_satisficing(&values, aspiration) {
        Some((index, value)) => println!("Satisficing option = {} value = {:.6}", index, value),
        None => println!("No option satisfies aspiration."),
    }
}
