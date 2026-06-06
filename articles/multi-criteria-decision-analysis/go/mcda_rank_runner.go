// mcda_rank_runner.go
// Run with: go run mcda_rank_runner.go

package main

import "fmt"

func weightedScore(scores []float64, weights []float64) float64 {
	total := 0.0
	for i := range scores {
		total += scores[i] * weights[i]
	}
	return total
}

func main() {
	scores := []float64{0.8, 0.6, 0.9}
	weights := []float64{0.3, 0.3, 0.4}
	fmt.Printf("Weighted score: %.6f\n", weightedScore(scores, weights))
}
