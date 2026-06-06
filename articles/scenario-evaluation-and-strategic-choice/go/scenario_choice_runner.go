// scenario_choice_runner.go
// Run with: go run scenario_choice_runner.go

package main

import "fmt"

func expectedValue(values []float64, probabilities []float64) float64 {
	total := 0.0
	for i := range values {
		total += values[i] * probabilities[i]
	}
	return total
}

func worstCase(values []float64) float64 {
	worst := values[0]
	for _, value := range values {
		if value < worst {
			worst = value
		}
	}
	return worst
}

func thresholdPassRate(values []float64, threshold float64) float64 {
	count := 0
	for _, value := range values {
		if value >= threshold {
			count++
		}
	}
	return float64(count) / float64(len(values))
}

func main() {
	values := []float64{0.78, 0.76, 0.82, 0.80, 0.81}
	probabilities := []float64{0.22, 0.24, 0.20, 0.18, 0.16}
	fmt.Printf("Expected value: %.6f\n", expectedValue(values, probabilities))
	fmt.Printf("Worst case: %.6f\n", worstCase(values))
	fmt.Printf("Threshold pass rate: %.6f\n", thresholdPassRate(values, 0.70))
}
