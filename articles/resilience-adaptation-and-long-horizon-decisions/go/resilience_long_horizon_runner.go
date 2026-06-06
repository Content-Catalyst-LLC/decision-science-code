// resilience_long_horizon_runner.go
// Run with: go run resilience_long_horizon_runner.go

package main

import "fmt"

func resilienceUpdate(current float64, recovery float64, investment float64, degradation float64, shock float64) float64 {
	next := current + recovery + investment - degradation - shock
	if next < 0 {
		return 0
	}
	return next
}

func resilientDecisionScore(longHorizonScore float64, averagePerformance float64, worstCase float64, passRate float64, performanceRange float64) float64 {
	return 0.30*longHorizonScore + 0.24*averagePerformance + 0.22*worstCase + 0.18*passRate - 0.06*performanceRange
}

func shouldRevise(systemState float64, resilienceCapacity float64, stressThreshold float64, resilienceThreshold float64) bool {
	return systemState >= stressThreshold || resilienceCapacity <= resilienceThreshold
}

func main() {
	fmt.Printf("Next resilience stock: %.6f\n", resilienceUpdate(35.0, 3.0, 2.0, 1.0, 1.6))
	fmt.Printf("Resilient decision score: %.6f\n", resilientDecisionScore(0.80, 0.79, 0.74, 1.0, 0.10))
	fmt.Printf("Revise? %t\n", shouldRevise(72.0, 24.0, 80.0, 25.0))
}
