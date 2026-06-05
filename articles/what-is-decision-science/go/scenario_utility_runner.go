// scenario_utility_runner.go
// Run with: go run scenario_utility_runner.go

package main

import (
	"fmt"
	"math"
)

func expectedValue(payoffs []float64, probabilities []float64) float64 {
	total := 0.0
	for i := range payoffs {
		total += payoffs[i] * probabilities[i]
	}
	return total
}

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
	probabilities := []float64{0.40, 0.35, 0.25}
	alternatives := map[string][]float64{
		"Optimize":        {120.0, 25.0, -80.0},
		"Hedge":           {90.0, 62.0, 12.0},
		"Preserve Option": {66.0, 58.0, 42.0},
	}

	for name, payoffs := range alternatives {
		fmt.Printf("%s | EV %.3f | EU %.6f\n", name, expectedValue(payoffs, probabilities), expectedUtility(payoffs, probabilities, 0.018))
	}
}
