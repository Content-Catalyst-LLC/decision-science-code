// alignment_score_runner.go
// Run with: go run alignment_score_runner.go

package main

import (
	"fmt"
	"math"
)

func weightedScore(scores []float64, weights []float64) float64 {
	total := 0.0
	for i := range scores {
		total += scores[i] * weights[i]
	}
	return total
}

func cosineSimilarity(a []float64, b []float64) float64 {
	dot := 0.0
	normA := 0.0
	normB := 0.0

	for i := range a {
		dot += a[i] * b[i]
		normA += a[i] * a[i]
		normB += b[i] * b[i]
	}

	return dot / (math.Sqrt(normA) * math.Sqrt(normB))
}

func main() {
	scores := []float64{0.86, 0.88, 0.82, 0.86, 0.89, 0.77}
	weights := []float64{0.16, 0.15, 0.17, 0.18, 0.18, 0.16}
	fmt.Printf("Decision quality score: %.6f\n", weightedScore(scores, weights))
	fmt.Printf("Cosine alignment: %.6f\n", cosineSimilarity([]float64{0.68, 0.88, 0.82, 0.93, 0.86}, []float64{0.20, 0.25, 0.18, 0.22, 0.15}))
}
