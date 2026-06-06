// complex_system_decision_runner.go
// Run with: go run complex_system_decision_runner.go

package main

import "fmt"

func complexSystemScore(adaptability float64, robustness float64, feedback float64, interdependence float64, burden float64, legitimacy float64, thresholdResilience float64) float64 {
	return 0.18*adaptability + 0.18*robustness + 0.16*feedback + 0.16*interdependence - 0.10*burden + 0.12*legitimacy + 0.20*thresholdResilience
}

func feedbackUpdate(state float64, reinforcing float64, balancing float64, disturbance float64) float64 {
	return state + reinforcing - balancing + disturbance
}

func main() {
	fmt.Printf("Complex-system score: %.6f\n", complexSystemScore(0.81, 0.86, 0.82, 0.83, 0.44, 0.78, 0.86))
	fmt.Printf("Next state: %.6f\n", feedbackUpdate(52.0, 3.0, 1.4, -0.2))
}
