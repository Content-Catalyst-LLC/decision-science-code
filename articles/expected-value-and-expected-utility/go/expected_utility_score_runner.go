// expected_utility_score_runner.go
// Run with: go run expected_utility_score_runner.go

package main

import (
	"fmt"
	"math"
)

func expectedValue(outcomes []float64, probabilities []float64) float64 {
	total := 0.0
	for i := range outcomes {
		total += outcomes[i] * probabilities[i]
	}
	return total
}

func crra(x float64, rho float64, offset float64) float64 {
	z := x + offset
	if math.Abs(rho-1.0) < 1e-9 {
		return math.Log(z)
	}
	return (math.Pow(z, 1.0-rho) - 1.0) / (1.0 - rho)
}

func expectedUtility(outcomes []float64, probabilities []float64, rho float64) float64 {
	total := 0.0
	for i := range outcomes {
		total += probabilities[i] * crra(outcomes[i], rho, 151.0)
	}
	return total
}

func main() {
	outcomes := []float64{180.0, 40.0}
	probabilities := []float64{0.60, 0.40}
	fmt.Printf("Expected value: %.4f\n", expectedValue(outcomes, probabilities))
	fmt.Printf("Expected utility rho=1: %.6f\n", expectedUtility(outcomes, probabilities, 1.0))
}
