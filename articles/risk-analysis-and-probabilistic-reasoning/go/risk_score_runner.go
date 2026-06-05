// risk_score_runner.go
// Run with: go run risk_score_runner.go

package main

import "fmt"

func expectedLoss(probabilities []float64, losses []float64) float64 {
	total := 0.0
	for i := range probabilities {
		total += probabilities[i] * losses[i]
	}
	return total
}

func bayesianUpdate(prior float64, sensitivity float64, falsePositiveRate float64) float64 {
	evidenceProbability := sensitivity*prior + falsePositiveRate*(1.0-prior)
	return (sensitivity * prior) / evidenceProbability
}

func main() {
	probabilities := []float64{0.08, 0.06, 0.03}
	losses := []float64{0.035, 0.040, 0.075}

	fmt.Printf("Expected loss: %.6f\n", expectedLoss(probabilities, losses))
	fmt.Printf("Posterior risk: %.6f\n", bayesianUpdate(0.10, 0.82, 0.12))
}
