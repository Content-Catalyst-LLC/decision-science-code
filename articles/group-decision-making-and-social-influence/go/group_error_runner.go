// group_error_runner.go
// Run with: go run group_error_runner.go

package main

import (
	"fmt"
	"math"
)

func collectiveError(groupEstimate float64, trueValue float64) float64 {
	return math.Abs(groupEstimate - trueValue)
}

func hiddenProfileRisk(sharedInformation float64, uniqueInformation float64) float64 {
	return uniqueInformation / (sharedInformation + uniqueInformation)
}

func main() {
	fmt.Printf("Collective error: %.6f\n", collectiveError(0.64, 0.62))
	fmt.Printf("Hidden-profile risk: %.6f\n", hiddenProfileRisk(5.0, 9.0))
}
