// historical_expected_utility_runner.go
// Run with: go run historical_expected_utility_runner.go

package main

import (
	"fmt"
	"math"
)

func utility(value float64, riskAversion float64) float64 {
	return 1.0 - math.Exp(-riskAversion*value)
}

func expectedUtility(payoffs []float64, probabilities []float64, riskAversion float64) float64 {
	total := 0.0
	for i := range payoffs {
		total += probabilities[i] * utility(payoffs[i], riskAversion)
	}
	return total
}

func main() {
	probabilities := []float64{0.42, 0.28, 0.18, 0.12}
	strategies := map[string][]float64{
		"Aggressive": {128, 50, -90, -20},
		"Balanced":  {92, 68, 18, 42},
		"Defensive": {62, 58, 44, 54},
		"Adaptive":  {88, 70, 36, 72},
	}

	for name, payoffs := range strategies {
		fmt.Printf("%s expected utility: %.6f\n", name, expectedUtility(payoffs, probabilities, 0.016))
	}
}
