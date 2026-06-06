// path_dependence_runner.go
// Run with: go run path_dependence_runner.go

package main

import "fmt"

func switchingCost(investment float64, networkDependence float64, institutionalRoutine float64) float64 {
	return 0.36*investment + 0.34*networkDependence + 0.30*institutionalRoutine
}

func lockInRisk(switchingCost float64, institutionalRoutine float64, networkDependence float64, optionValue float64) float64 {
	return 0.42*switchingCost + 0.28*institutionalRoutine + 0.20*networkDependence - 0.10*optionValue
}

func shouldReview(lockInRisk float64, optionValue float64, lockInThreshold float64, optionThreshold float64) bool {
	return lockInRisk >= lockInThreshold || optionValue <= optionThreshold
}

func main() {
	cost := switchingCost(0.55, 0.62, 0.58)
	risk := lockInRisk(cost, 0.62, 0.55, 0.40)
	fmt.Printf("Switching cost: %.6f\n", cost)
	fmt.Printf("Lock-in risk: %.6f\n", risk)
	fmt.Printf("Review? %t\n", shouldReview(risk, 0.40, 0.72, 0.35))
}
