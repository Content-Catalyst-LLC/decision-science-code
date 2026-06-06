// systems_modeling_runner.go
// Run with: go run systems_modeling_runner.go

package main

import "fmt"

func stockUpdate(stock float64, inflow float64, outflow float64) float64 {
	return stock + inflow - outflow
}

func feedbackUpdate(state float64, reinforcing float64, balancing float64, disturbance float64) float64 {
	return state + reinforcing - balancing + disturbance
}

func systemsDecisionScore(dynamicScore float64, averagePerformance float64, worstCase float64, thresholdPassRate float64) float64 {
	return 0.35*dynamicScore + 0.25*averagePerformance + 0.20*worstCase + 0.20*thresholdPassRate
}

func main() {
	fmt.Printf("Next stock: %.6f\n", stockUpdate(100.0, 12.0, 8.5))
	fmt.Printf("Next state: %.6f\n", feedbackUpdate(55.0, 3.85, 2.10, -0.4))
	fmt.Printf("Systems decision score: %.6f\n", systemsDecisionScore(0.78, 0.82, 0.79, 1.0))
}
