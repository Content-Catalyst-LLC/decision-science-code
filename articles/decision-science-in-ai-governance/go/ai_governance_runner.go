// ai_governance_runner.go
// Run with: go run ai_governance_runner.go

package main

import (
	"fmt"
	"math"
)

func compositeAIRisk(safety float64, equity float64, bias float64, privacy float64, opacity float64, security float64) float64 {
	return 0.20*safety + 0.18*equity + 0.16*bias + 0.16*privacy + 0.14*opacity + 0.16*security
}

func driftIndicator(currentMetric float64, baselineMetric float64) float64 {
	return math.Abs(currentMetric - baselineMetric)
}

func main() {
	fmt.Printf("Composite AI risk: %.6f\n", compositeAIRisk(0.52, 0.48, 0.50, 0.42, 0.55, 0.46))
	fmt.Printf("Drift indicator: %.6f\n", driftIndicator(0.77, 0.86))
}
