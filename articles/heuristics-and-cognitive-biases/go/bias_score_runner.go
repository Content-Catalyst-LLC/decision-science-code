// bias_score_runner.go
// Run with: go run bias_score_runner.go

package main

import (
	"fmt"
	"math"
)

func anchoredEstimate(anchor float64, evidence float64, weight float64) float64 {
	return weight*anchor + (1.0-weight)*evidence
}

func brierScore(probability float64, outcome float64) float64 {
	return math.Pow(probability-outcome, 2)
}

func main() {
	fmt.Printf("Anchored estimate: %.6f\n", anchoredEstimate(0.80, 0.42, 0.45))
	fmt.Printf("Brier score: %.6f\n", brierScore(0.72, 1.0))
}
