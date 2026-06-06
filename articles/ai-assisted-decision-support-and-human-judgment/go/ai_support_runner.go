// ai_support_runner.go
// Run with: go run ai_support_runner.go

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

func justifiedModelReliance(evidenceQuality float64, calibration float64, decisionRisk float64, uncertainty float64) float64 {
	return clamp(0.35*evidenceQuality+0.35*calibration-0.16*decisionRisk-0.14*uncertainty, 0.0, 1.0)
}

func automationBias(actualReliance float64, justifiedReliance float64) float64 {
	return actualReliance - justifiedReliance
}

func main() {
	justified := justifiedModelReliance(0.82, 0.78, 0.54, 0.36)
	fmt.Printf("Justified model reliance: %.6f\n", justified)
	fmt.Printf("Automation bias: %.6f\n", automationBias(0.78, justified))
}
