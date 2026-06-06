// ai_support_cli.rs
// Compile with: rustc ai_support_cli.rs -o ai_support_cli

fn justified_model_reliance(evidence_quality: f64, calibration: f64, decision_risk: f64, uncertainty: f64) -> f64 {
    (0.35 * evidence_quality + 0.35 * calibration - 0.16 * decision_risk - 0.14 * uncertainty).clamp(0.0, 1.0)
}

fn automation_bias(actual_reliance: f64, justified_reliance: f64) -> f64 {
    actual_reliance - justified_reliance
}

fn main() {
    let justified = justified_model_reliance(0.82, 0.78, 0.54, 0.36);
    println!("Justified model reliance = {:.6}", justified);
    println!("Automation bias = {:.6}", automation_bias(0.78, justified));
}
