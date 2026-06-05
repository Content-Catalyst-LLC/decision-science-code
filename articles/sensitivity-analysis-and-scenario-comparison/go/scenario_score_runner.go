// scenario_score_runner.go
// Run with: go run scenario_score_runner.go

package main

import (
	"fmt"
	"math"
)

func strategyScore(base, demandSensitivity, costSensitivity, disruptionSensitivity, resilienceBuffer, adaptationCapacity, demand, cost, disruption float64) float64 {
	return base +
		demandSensitivity*demand -
		costSensitivity*cost -
		disruptionSensitivity*disruption +
		resilienceBuffer*math.Max(0.0, disruption) +
		adaptationCapacity*math.Abs(demand)
}

func main() {
	balanced := strategyScore(75.0, 8.0, 10.0, 11.0, 9.0, 7.0, 0.5, 0.3, 0.2)
	adaptive := strategyScore(73.0, 7.0, 9.0, 9.0, 12.0, 12.0, 0.5, 0.3, 0.2)

	fmt.Printf("Balanced score: %.4f\n", balanced)
	fmt.Printf("Adaptive score: %.4f\n", adaptive)
}
