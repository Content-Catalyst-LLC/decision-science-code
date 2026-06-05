// accountability_score_runner.go
// Run with: go run accountability_score_runner.go

package main

import "fmt"

func weightedScore(scores []float64, weights []float64) float64 {
	total := 0.0
	for i := range scores {
		total += scores[i] * weights[i]
	}
	return total
}

func minimum(values []float64) float64 {
	min := values[0]
	for _, value := range values {
		if value < min {
			min = value
		}
	}
	return min
}

func main() {
	weights := []float64{0.10, 0.09, 0.11, 0.11, 0.12, 0.10, 0.09, 0.10, 0.09, 0.09, 0.10}
	record := []float64{0.91, 0.88, 0.80, 0.89, 0.92, 0.86, 0.84, 0.88, 0.90, 0.92, 0.90}
	quality := weightedScore(record, weights)
	accountable := 0.70*quality + 0.30*minimum(record)
	fmt.Printf("Accountable judgment score: %.4f\n", accountable)
}
