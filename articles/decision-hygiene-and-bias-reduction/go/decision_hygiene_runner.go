// decision_hygiene_runner.go
// Run with: go run decision_hygiene_runner.go

package main

import (
	"fmt"
	"math"
)

func bias(errors []float64) float64 {
	total := 0.0
	for _, value := range errors {
		total += value
	}
	return total / float64(len(errors))
}

func mse(errors []float64) float64 {
	total := 0.0
	for _, value := range errors {
		total += value * value
	}
	return total / float64(len(errors))
}

func brierScore(probability float64, outcome float64) float64 {
	return math.Pow(probability-outcome, 2)
}

func main() {
	errors := []float64{0.12, 0.04, -0.03, 0.08}
	fmt.Printf("Bias: %.6f\n", bias(errors))
	fmt.Printf("MSE: %.6f\n", mse(errors))
	fmt.Printf("Brier score: %.6f\n", brierScore(0.69, 0.0))
}
