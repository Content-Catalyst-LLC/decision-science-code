fn crisis_risk(likelihood: f64, severity: f64, exposure: f64, vulnerability: f64, criticality: f64) -> f64 {
    likelihood * severity * exposure * vulnerability * criticality
}

fn main() {
    println!("Crisis risk = {:.6}", crisis_risk(0.72, 0.86, 0.68, 0.62, 0.90));
}
