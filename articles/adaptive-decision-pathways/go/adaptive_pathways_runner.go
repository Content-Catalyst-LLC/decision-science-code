// adaptive_pathways_runner.go
// Run with: go run adaptive_pathways_runner.go

package main

import "fmt"

func pathwayScore(initialPerformance float64, flexibility float64, monitoringQuality float64, triggerClarity float64, switchingCost float64, fallbackStrength float64) float64 {
	return 0.20*initialPerformance + 0.18*flexibility + 0.16*monitoringQuality + 0.16*triggerClarity - 0.12*switchingCost + 0.18*fallbackStrength
}

func triggerHit(systemStress float64, optionValue float64, stressTrigger float64, optionValueTrigger float64) bool {
	return systemStress >= stressTrigger || optionValue <= optionValueTrigger
}

func main() {
	score := pathwayScore(0.76, 0.88, 0.82, 0.80, 0.38, 0.84)
	fmt.Printf("Pathway score: %.6f\n", score)
	fmt.Printf("Trigger hit? %t\n", triggerHit(0.70, 0.55, 0.68, 0.40))
}
