// tradeoff_rank_runner.go
// Run with: go run tradeoff_rank_runner.go

package main

import "fmt"

func weightedScore(scores []float64, weights []float64) float64 {
	total := 0.0
	for i := range scores {
		total += scores[i] * weights[i]
	}
	return total
}

func regret(score float64, bestScore float64) float64 {
	return bestScore - score
}

func main() {
	scores := []float64{0.90, 0.38, 0.42, 0.54, 0.48, 0.70}
	weights := []float64{0.18, 0.18, 0.20, 0.18, 0.14, 0.12}
	fmt.Printf("Weighted score: %.6f\n", weightedScore(scores, weights))
	fmt.Printf("Regret: %.6f\n", regret(0.72, 0.91))
}
