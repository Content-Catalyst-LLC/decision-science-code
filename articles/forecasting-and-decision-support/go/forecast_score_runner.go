// forecast_score_runner.go
// Run with: go run forecast_score_runner.go

package main

import (
	"fmt"
	"math"
)

func brierScore(probability float64, outcome float64) float64 {
	return math.Pow(probability-outcome, 2)
}

func thresholdFromCosts(falsePositiveCost float64, falseNegativeCost float64) float64 {
	return falsePositiveCost / (falsePositiveCost + falseNegativeCost)
}

func main() {
	fmt.Printf("Brier score: %.6f\n", brierScore(0.62, 1.0))
	fmt.Printf("Decision threshold: %.6f\n", thresholdFromCosts(15.0, 85.0))
}
