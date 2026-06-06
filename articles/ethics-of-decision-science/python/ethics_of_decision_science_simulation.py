#!/usr/bin/env python3
from pathlib import Path
import csv, json, random
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
TABLES = ROOT / "outputs" / "tables"
RECORDS = ROOT / "outputs" / "decision_records"

CONTEXTS = {
    "Public Policy Allocation": (0.44, 0.64, 0.68, 0.62, 0.42, 0.70, 0.48),
    "AI-Supported Eligibility": (0.56, 0.54, 0.58, 0.46, 0.60, 0.62, 0.64),
    "Infrastructure Siting": (0.50, 0.58, 0.60, 0.56, 0.58, 0.66, 0.58),
    "Crisis Triage": (0.60, 0.52, 0.56, 0.50, 0.66, 0.68, 0.72),
}

def read_params():
    with (DATA / "synthetic_system_parameters.csv").open("r", encoding="utf-8", newline="") as f:
        return {r["parameter"]: float(r["value"]) for r in csv.DictReader(f)}

def write_csv(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(data[0].keys()))
        w.writeheader()
        w.writerows(data)

def main():
    p = read_params()
    random.seed(int(p["random_seed"]))
    rows = []
    for name, cfg in CONTEXTS.items():
        ethical_risk, trust, accountability, contestability, burden, adaptability, harm_pressure = cfg
        for t in range(1, int(p["time_steps"]) + 1):
            event = random.random() < 0.16
            sev = random.uniform(0.08, 0.28) if event else random.uniform(0.00, 0.05)
            burden = max(0.0, min(1.0, burden + 0.06 * sev + 0.020 * harm_pressure - 0.018 * adaptability + random.gauss(0, 0.018)))
            accountability = max(0.0, min(1.0, accountability - 0.020 * sev + 0.010 * adaptability + random.gauss(0, 0.014)))
            contestability = max(0.0, min(1.0, contestability - 0.016 * sev + 0.012 * accountability + random.gauss(0, 0.014)))
            trust = max(0.0, min(1.0, trust - 0.035 * sev - 0.020 * burden + 0.018 * accountability + 0.014 * contestability + random.gauss(0, 0.018)))
            ethical_risk = max(0.0, min(1.0, ethical_risk + 0.12 * burden + 0.10 * harm_pressure + 0.12 * max(0, p["accountability_trigger"] - accountability) + 0.12 * max(0, p["contestability_trigger"] - contestability) - 0.08 * trust - 0.08 * adaptability + 0.08 * sev + random.gauss(0, 0.018)))
            review = ethical_risk >= p["ethical_risk_trigger"] or trust <= p["trust_trigger"] or accountability <= p["accountability_trigger"] or contestability <= p["contestability_trigger"] or burden >= p["burden_trigger"]
            if review:
                accountability = min(1.0, accountability + 0.045)
                contestability = min(1.0, contestability + 0.040)
                trust = min(1.0, trust + 0.025)
                ethical_risk = max(0.0, ethical_risk - 0.055 * adaptability)
            rows.append({
                "decision_context": name,
                "time": t,
                "ethical_risk": round(ethical_risk, 6),
                "stakeholder_trust": round(trust, 6),
                "accountability_strength": round(accountability, 6),
                "contestability": round(contestability, 6),
                "distributional_burden": round(burden, 6),
                "controversy_event": event,
                "controversy_severity": round(sev, 6),
                "review_required": review,
            })
    write_csv(TABLES / "ethical_decision_timeseries.csv", rows)
    summary = []
    for name in sorted(CONTEXTS):
        r = [x for x in rows if x["decision_context"] == name]
        summary.append({
            "decision_context": name,
            "maximum_ethical_risk": round(max(float(x["ethical_risk"]) for x in r), 6),
            "minimum_stakeholder_trust": round(min(float(x["stakeholder_trust"]) for x in r), 6),
            "minimum_accountability_strength": round(min(float(x["accountability_strength"]) for x in r), 6),
            "minimum_contestability": round(min(float(x["contestability"]) for x in r), 6),
            "maximum_distributional_burden": round(max(float(x["distributional_burden"]) for x in r), 6),
            "review_required_count": sum(1 for x in r if x["review_required"]),
        })
    write_csv(TABLES / "ethical_decision_summary.csv", summary)
    RECORDS.mkdir(parents=True, exist_ok=True)
    (RECORDS / "ethical_decision_record.json").write_text(json.dumps({
        "article": "Ethics of Decision Science",
        "decision_context": "Simulating ethical risk, stakeholder trust, accountability, contestability, distributional burden, and review triggers.",
        "parameters": p,
        "summary_metrics": summary
    }, indent=2), encoding="utf-8")
    print(TABLES / "ethical_decision_timeseries.csv")
    print(TABLES / "ethical_decision_summary.csv")
    print(RECORDS / "ethical_decision_record.json")

if __name__ == "__main__":
    main()
