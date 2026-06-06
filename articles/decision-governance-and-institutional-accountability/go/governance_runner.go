// governance_runner.go
// Run with: go run governance_runner.go

package main

import "fmt"

func accountabilityScore(decisionRights float64, traceability float64, review float64, ownership float64, monitoring float64, corrective float64) float64 {
	return 0.18*decisionRights + 0.17*traceability + 0.18*review + 0.17*ownership + 0.15*monitoring + 0.15*corrective
}

func responsibilityGap(influence float64, accountability float64) float64 {
	gap := influence - accountability
	if gap < 0 {
		return 0
	}
	return gap
}

func main() {
	fmt.Printf("Accountability score: %.6f\n", accountabilityScore(0.82, 0.86, 0.88, 0.84, 0.90, 0.92))
	fmt.Printf("Responsibility gap: %.6f\n", responsibilityGap(0.62, 0.34))
}
