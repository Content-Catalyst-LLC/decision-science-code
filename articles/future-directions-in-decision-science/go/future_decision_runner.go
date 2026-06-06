// future_decision_runner.go
// Run with: go run future_decision_runner.go

package main

import "fmt"

func clamp(v float64, low float64, high float64) float64 {
	if v < low {
		return low
	}
	if v > high {
		return high
	}
	return v
}

func futureMaturity(ai float64, governance float64, uncertainty float64, legitimacy float64, reproducibility float64, systems float64, ethics float64, adaptive float64, failure float64) float64 {
	return clamp(0.12*ai+0.14*governance+0.14*uncertainty+0.12*legitimacy+0.12*reproducibility+0.12*systems+0.14*ethics+0.14*adaptive-0.14*failure, 0.0, 1.0)
}

func main() {
	fmt.Printf("Future maturity: %.6f\n", futureMaturity(0.86, 0.90, 0.88, 0.84, 0.88, 0.86, 0.90, 0.88, 0.24))
}
