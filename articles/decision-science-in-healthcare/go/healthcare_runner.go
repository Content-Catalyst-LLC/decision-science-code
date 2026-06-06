// healthcare_runner.go
// Run with: go run healthcare_runner.go

package main

import "fmt"

func treatmentValueScore(expectedBenefit float64, adverseEventRisk float64, costBurden float64, patientPreferenceFit float64, equityScore float64, implementationFeasibility float64) float64 {
	return 0.30*expectedBenefit - 0.18*adverseEventRisk - 0.14*costBurden + 0.18*patientPreferenceFit + 0.10*equityScore + 0.10*implementationFeasibility
}

func queueNext(currentQueue float64, arrivals float64, discharges float64) float64 {
	next := currentQueue + arrivals - discharges
	if next < 0 {
		return 0
	}
	return next
}

func main() {
	score := treatmentValueScore(0.72, 0.12, 0.54, 0.88, 0.76, 0.70)
	fmt.Printf("Treatment value score: %.6f\n", score)
	fmt.Printf("Queue next: %.6f\n", queueNext(18.0, 24.0, 22.0))
}
