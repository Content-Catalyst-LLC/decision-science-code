#!/usr/bin/env python3
from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
TABLES = ROOT / "outputs" / "tables"

def rows(path):
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(data[0].keys()))
        w.writeheader()
        w.writerows(data)

def main():
    out = []
    for r in rows(DATA / "synthetic_ethical_decision_alternatives.csv"):
        expected_value = float(r["expected_value"])
        equity = float(r["equity_score"])
        safety = float(r["safety_score"])
        legitimacy = float(r["legitimacy_score"])
        transparency = float(r["transparency_score"])
        contestability = float(r["contestability_score"])
        reversibility = float(r["reversibility_score"])
        accountability = float(r["accountability_score"])
        harm = float(r["harm_risk"])
        opacity = float(r["opacity_risk"])
        exclusion = float(r["exclusion_risk"])
        ethical_value = (
            0.18 * expected_value / 100 + 0.18 * equity + 0.16 * safety + 0.14 * legitimacy +
            0.10 * transparency + 0.10 * contestability + 0.08 * reversibility + 0.06 * accountability
        )
        ethical_risk = 0.34 * harm + 0.22 * opacity + 0.24 * exclusion + 0.20 * (1 - accountability)
        net = ethical_value - 0.42 * ethical_risk
        review = equity < 0.55 or safety < 0.55 or legitimacy < 0.55 or contestability < 0.55 or ethical_risk > 0.55
        out.append({
            "alternative": r["alternative"],
            "ethical_value_score": round(ethical_value, 6),
            "ethical_risk_score": round(ethical_risk, 6),
            "net_ethical_score": round(net, 6),
            "review_flag": "review" if review else "acceptable",
        })
    out.sort(key=lambda x: x["net_ethical_score"], reverse=True)
    for i, r in enumerate(out, 1):
        r["rank"] = i
    write(TABLES / "ethical_decision_results.csv", out)
    print(TABLES / "ethical_decision_results.csv")

if __name__ == "__main__":
    main()
