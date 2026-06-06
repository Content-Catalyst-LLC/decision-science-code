// stakeholder_legitimacy_runner.go
// Run with: go run stakeholder_legitimacy_runner.go

package main

import "fmt"

func weightedScore(values []float64, weights []float64) float64 {
	total := 0.0
	for i := range values {
		total += values[i] * weights[i]
	}
	return total
}

func legitimacyIndex(aggregateScore float64, proceduralScore float64, passRate float64, minScore float64, maxBurden float64) float64 {
	return 0.40*aggregateScore + 0.24*proceduralScore + 0.18*passRate + 0.10*minScore - 0.08*maxBurden
}

func main() {
	values := []float64{0.68, 0.80, 0.84, 0.82, 0.86, 0.90}
	weights := []float64{0.12, 0.18, 0.28, 0.14, 0.16, 0.12}
	fmt.Printf("Stakeholder score: %.6f\n", weightedScore(values, weights))
	fmt.Printf("Legitimacy index: %.6f\n", legitimacyIndex(0.82, 0.89, 1.0, 0.76, 0.26))
}
