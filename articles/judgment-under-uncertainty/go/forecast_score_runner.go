// forecast_score_runner.go
// Run with: go run forecast_score_runner.go

package main

import (
	"fmt"
	"math"
)

func posteriorFromLikelihoods(prior float64, likelihoodTrue float64, likelihoodFalse float64) float64 {
	odds := prior / (1.0 - prior)
	posteriorOdds := odds * (likelihoodTrue / likelihoodFalse)
	return posteriorOdds / (1.0 + posteriorOdds)
}

func brierScore(probability float64, outcome float64) float64 {
	return math.Pow(probability-outcome, 2)
}

func main() {
	fmt.Printf("Posterior: %.6f\n", posteriorFromLikelihoods(0.35, 0.72, 0.28))
	fmt.Printf("Brier score: %.6f\n", brierScore(0.62, 1.0))
}
