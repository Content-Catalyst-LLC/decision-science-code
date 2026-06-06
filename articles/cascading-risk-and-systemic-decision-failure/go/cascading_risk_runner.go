// cascading_risk_runner.go
// Run with: go run cascading_risk_runner.go

package main

import "fmt"

func maxFloat(a float64, b float64) float64 {
	if a > b {
		return a
	}
	return b
}

func cascadeRiskScore(exposure float64, dependencyCentrality float64, bufferWeakness float64, commonModeRisk float64, monitoringQuality float64, responseCapacity float64) float64 {
	return 0.22*exposure + 0.22*dependencyCentrality + 0.20*bufferWeakness + 0.18*commonModeRisk - 0.09*monitoringQuality - 0.09*responseCapacity
}

func thresholdFailure(stress float64, neighborFailureLoad float64, buffer float64, threshold float64) bool {
	effectiveStress := stress + neighborFailureLoad + maxFloat(0.0, 0.40-buffer)
	return effectiveStress >= threshold
}

func main() {
	score := cascadeRiskScore(0.82, 0.88, 0.76, 0.79, 0.42, 0.40)
	fmt.Printf("Cascade risk score: %.6f\n", score)
	fmt.Printf("Threshold failure? %t\n", thresholdFailure(0.52, 0.18, 0.31, 0.66))
}
