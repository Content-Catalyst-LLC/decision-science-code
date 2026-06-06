// value_of_information_runner.go
// Run with: go run value_of_information_runner.go

package main

import "fmt"

func expectedValue(values []float64, probabilities []float64) float64 {
	total := 0.0
	for i := range values {
		total += values[i] * probabilities[i]
	}
	return total
}

func evpi(perfectInformationValue float64, currentExpectedValue float64) float64 {
	return perfectInformationValue - currentExpectedValue
}

func netValueWaiting(evsi float64, informationCost float64, delayCost float64) float64 {
	return evsi - informationCost - delayCost
}

func main() {
	values := []float64{82.0, 28.0, 40.0, 76.0}
	probabilities := []float64{0.35, 0.25, 0.20, 0.20}
	fmt.Printf("Expected value: %.6f\n", expectedValue(values, probabilities))
	fmt.Printf("EVPI: %.6f\n", evpi(76.4, 68.1))
	fmt.Printf("Net value waiting: %.6f\n", netValueWaiting(4.4, 2.0, 1.3))
}
