// bayesian_update_runner.go
// Run with: go run bayesian_update_runner.go

package main

import "fmt"

func bayesianUpdate(prior float64, sensitivity float64, falsePositiveRate float64) float64 {
	numerator := sensitivity * prior
	denominator := numerator + falsePositiveRate*(1.0-prior)
	return numerator / denominator
}

func posteriorExpectedUtility(posterior float64, utilityTrue float64, utilityFalse float64) float64 {
	return posterior*utilityTrue + (1.0-posterior)*utilityFalse
}

func main() {
	posterior := bayesianUpdate(0.10, 0.86, 0.12)
	actionUtility := posteriorExpectedUtility(posterior, 90.0, -25.0)
	waitUtility := posteriorExpectedUtility(posterior, -80.0, 15.0)

	fmt.Printf("Posterior: %.6f\n", posterior)
	fmt.Printf("Action utility: %.6f\n", actionUtility)
	fmt.Printf("Wait utility: %.6f\n", waitUtility)
}
