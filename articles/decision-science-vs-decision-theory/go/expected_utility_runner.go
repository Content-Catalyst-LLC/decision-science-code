// expected_utility_runner.go
// Run with: go run expected_utility_runner.go

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
	probabilities := []float64{0.22, 0.34, 0.18, 0.16, 0.10}
	strategies := map[string][]float64{
		"Optimize": {145, 92, 30, -95, -40},
		"Balanced": {112, 84, 58, 12, 30},
		"Robust": {78, 72, 65, 48, 55},
	}

	for name, payoffs := range strategies {
		fmt.Printf("%s expected utility: %.6f\n", name, expectedUtility(payoffs, probabilities, 0.018))
	}
}
