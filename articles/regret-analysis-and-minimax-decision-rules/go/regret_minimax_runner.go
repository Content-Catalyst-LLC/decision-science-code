// regret_minimax_runner.go
// Run with: go run regret_minimax_runner.go

package main

import "fmt"

func expectedValue(values []float64, weights []float64) float64 {
	total := 0.0
	for i := range values {
		total += values[i] * weights[i]
	}
	return total
}

func maximinValue(values []float64) float64 {
	worst := values[0]
	for _, value := range values {
		if value < worst {
			worst = value
		}
	}
	return worst
}

func maximumRegret(regrets []float64) float64 {
	maxValue := regrets[0]
	for _, value := range regrets {
		if value > maxValue {
			maxValue = value
		}
	}
	return maxValue
}

func main() {
	values := []float64{0.73, 0.81, 0.79, 0.87, 0.76, 0.77}
	weights := []float64{0.18, 0.16, 0.18, 0.17, 0.15, 0.16}
	regrets := []float64{0.19, 0.00, 0.05, 0.01, 0.06, 0.06}
	fmt.Printf("Expected value: %.6f\n", expectedValue(values, weights))
	fmt.Printf("Maximin value: %.6f\n", maximinValue(values))
	fmt.Printf("Maximum regret: %.6f\n", maximumRegret(regrets))
}
