// robust_scenario_runner.go
// Run with: go run robust_scenario_runner.go

package main

import "fmt"

func robustness(payoffs []float64, threshold float64) float64 {
	count := 0
	for _, value := range payoffs {
		if value >= threshold {
			count++
		}
	}
	return float64(count) / float64(len(payoffs))
}

func main() {
	strategies := map[string][]float64{
		"Expand":          {120, 45, -95, -130, 20},
		"Hedge":           {92, 68, 18, -20, 55},
		"Preserve Option": {72, 62, 42, 18, 70},
		"Adaptive Pathway": {95, 72, 34, 10, 78},
	}

	for name, payoffs := range strategies {
		fmt.Printf("%s robustness: %.3f\n", name, robustness(payoffs, 40.0))
	}
}
