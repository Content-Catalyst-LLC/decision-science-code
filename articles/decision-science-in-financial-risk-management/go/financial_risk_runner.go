// financial_risk_runner.go
// Run with: go run financial_risk_runner.go

package main

import "fmt"

func expectedLoss(losses []float64, probabilities []float64) float64 {
	total := 0.0
	for i := range losses {
		total += losses[i] * probabilities[i]
	}
	return total
}

func capitalNext(currentCapital float64, periodReturnPct float64, floor float64) float64 {
	next := currentCapital * (1.0 + periodReturnPct/100.0)
	if next < floor {
		return floor
	}
	return next
}

func main() {
	losses := []float64{-1.2, -4.8, -3.6, -6.2}
	probs := []float64{0.55, 0.20, 0.15, 0.10}
	fmt.Printf("Expected loss: %.6f\n", expectedLoss(losses, probs))
	fmt.Printf("Capital next: %.6f\n", capitalNext(100.0, -8.5, 20.0))
}
