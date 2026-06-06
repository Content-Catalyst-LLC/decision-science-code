// infrastructure_runner.go
// Run with: go run infrastructure_runner.go

package main

import "fmt"

func expectedValue(values []float64, probabilities []float64) float64 {
	total := 0.0
	for i := range values {
		total += values[i] * probabilities[i]
	}
	return total
}

func triggerReached(indicator float64, threshold float64) bool {
	return indicator >= threshold
}

func main() {
	values := []float64{76.0, 76.0, 82.0, 70.0, 78.0}
	probabilities := []float64{0.30, 0.20, 0.20, 0.15, 0.15}
	fmt.Printf("Expected service value: %.6f\n", expectedValue(values, probabilities))
	fmt.Printf("Adaptive trigger reached: %t\n", triggerReached(0.74, 0.70))
}
