// process_outcome_score_runner.go
// Run with: go run process_outcome_score_runner.go

package main

import "fmt"

func weightedScore(scores []float64, weights []float64) float64 {
	total := 0.0
	for i := range scores {
		total += scores[i] * weights[i]
	}
	return total
}

func classify(processScore float64, outcome float64) string {
	goodProcess := processScore >= 0.80
	goodOutcome := outcome >= 75.0
	if goodProcess && goodOutcome {
		return "good process and good outcome"
	}
	if goodProcess && !goodOutcome {
		return "good process exposed to unfavorable uncertainty"
	}
	if !goodProcess && goodOutcome {
		return "weak process with favorable outcome; possible luck"
	}
	return "weak process and weak outcome"
}

func main() {
	weights := []float64{0.11, 0.10, 0.12, 0.13, 0.11, 0.10, 0.11, 0.11, 0.11}
	scores := []float64{0.92, 0.90, 0.94, 0.90, 0.88, 0.86, 0.82, 0.94, 0.96}
	score := weightedScore(scores, weights)
	fmt.Printf("Staged Learning Decision quality: %.4f\n", score)
	fmt.Println(classify(score, 62.0))
}
