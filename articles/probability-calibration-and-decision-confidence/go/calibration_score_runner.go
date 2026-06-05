// calibration_score_runner.go
// Run with: go run calibration_score_runner.go

package main

import (
	"fmt"
	"math"
)

func clamp(value float64, low float64, high float64) float64 {
	return math.Max(low, math.Min(high, value))
}

func brierScore(probability float64, outcome float64) float64 {
	return math.Pow(probability-outcome, 2)
}

func logLoss(probability float64, outcome float64) float64 {
	p := clamp(probability, 0.01, 0.99)
	return -(outcome*math.Log(p) + (1.0-outcome)*math.Log(1.0-p))
}

func main() {
	fmt.Printf("Brier score: %.6f\n", brierScore(0.72, 1.0))
	fmt.Printf("Log loss: %.6f\n", logLoss(0.72, 1.0))
}
