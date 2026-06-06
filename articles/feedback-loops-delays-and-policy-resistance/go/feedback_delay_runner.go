// feedback_delay_runner.go
// Run with: go run feedback_delay_runner.go

package main

import "fmt"

func feedbackUpdate(state float64, reinforcing float64, balancing float64, resistance float64, disturbance float64) float64 {
	return state + reinforcing - balancing + resistance + disturbance
}

func netPolicyEffect(policyDelta float64, intendedStrength float64, resistanceStrength float64, resistanceResponse float64) float64 {
	return intendedStrength*policyDelta - resistanceStrength*resistanceResponse
}

func feedbackAdjustedScore(dynamicScore float64, averagePerformance float64, worstCase float64, thresholdPassRate float64) float64 {
	return 0.35*dynamicScore + 0.25*averagePerformance + 0.20*worstCase + 0.20*thresholdPassRate
}

func main() {
	fmt.Printf("Next state: %.6f\n", feedbackUpdate(50.0, 4.0, 1.12, 0.4, -0.3))
	fmt.Printf("Net policy effect: %.6f\n", netPolicyEffect(10.0, 0.8, 0.4, 6.0))
	fmt.Printf("Feedback-adjusted score: %.6f\n", feedbackAdjustedScore(0.42, 0.79, 0.76, 1.0))
}
