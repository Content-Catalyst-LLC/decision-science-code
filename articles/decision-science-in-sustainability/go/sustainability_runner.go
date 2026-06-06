// sustainability_runner.go
// Run with: go run sustainability_runner.go

package main

import "fmt"

func sustainabilityValueScore(emissionsReduction float64, socialEquity float64, costBurden float64, resilienceScore float64, implementationFeasibility float64, thresholdProtection float64) float64 {
	return 0.22*emissionsReduction + 0.20*socialEquity - 0.12*costBurden + 0.18*resilienceScore + 0.12*implementationFeasibility + 0.16*thresholdProtection
}

func thresholdBreach(resourceStock float64, threshold float64) bool {
	return resourceStock < threshold
}

func main() {
	score := sustainabilityValueScore(0.61, 0.74, 0.49, 0.82, 0.66, 0.82)
	fmt.Printf("Sustainability value score: %.6f\n", score)
	fmt.Printf("Threshold breach? %t\n", thresholdBreach(34.0, 35.0))
}
