// organizational_strategy_runner.go
// Run with: go run organizational_strategy_runner.go

package main

import "fmt"

func expectedValue(values []float64, probabilities []float64) float64 {
	total := 0.0
	for i := range values {
		total += values[i] * probabilities[i]
	}
	return total
}

func robustStrategyScore(expectedValue float64, downsideRobustness float64, adaptability float64, reversibility float64) float64 {
	return 0.36*expectedValue/100.0 + 0.30*downsideRobustness/100.0 + 0.20*adaptability + 0.14*reversibility
}

func main() {
	values := []float64{68.0, 82.0, 89.0, 66.0}
	probabilities := []float64{0.25, 0.35, 0.20, 0.20}
	ev := expectedValue(values, probabilities)
	fmt.Printf("Expected strategic value: %.6f\n", ev)
	fmt.Printf("Robust strategy score: %.6f\n", robustStrategyScore(ev, 66.0, 0.84, 0.82))
}
