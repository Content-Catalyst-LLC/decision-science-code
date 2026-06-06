// calibration_score_runner.go
// Run with: go run calibration_score_runner.go

package main

import (
	"fmt"
	"math"
)

func brierScore(probability float64, outcome float64) float64 {
	return math.Pow(probability-outcome, 2)
}

func confidenceError(confidence float64, accuracyProxy float64) float64 {
	return confidence - accuracyProxy
}

func planningError(actual float64, estimate float64) float64 {
	return (actual - estimate) / estimate
}

func main() {
	fmt.Printf("Brier score: %.6f\n", brierScore(0.69, 0.0))
	fmt.Printf("Confidence error: %.6f\n", confidenceError(0.88, 0.52))
	fmt.Printf("Planning error: %.6f\n", planningError(520.0, 365.0))
}
