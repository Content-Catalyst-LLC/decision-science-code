// decision_quality_score_runner.go
// Run with: go run decision_quality_score_runner.go

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
	weights := []float64{0.12, 0.14, 0.12, 0.10, 0.11, 0.14, 0.12, 0.08, 0.07}
	scores := []float64{0.88, 0.87, 0.85, 0.84, 0.86, 0.86, 0.93, 0.84, 0.88}
	fmt.Printf("Adaptive Learning Strategy score: %.4f\n", weightedScore(scores, weights))
}
