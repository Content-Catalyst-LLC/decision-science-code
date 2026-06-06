// democratic_reasoning_runner.go
// Run with: go run democratic_reasoning_runner.go

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

func legitimacyScore(transparency float64, participation float64, fairness float64, evidence float64, contestability float64, accountability float64) float64 {
	return 0.17*transparency + 0.17*participation + 0.18*fairness + 0.16*evidence + 0.16*contestability + 0.16*accountability
}

func nextTrust(current float64, performance float64, transparency float64, responsiveness float64, fairness float64, uncertainty float64, harm float64) float64 {
	return clamp(current+0.08*performance+0.06*transparency+0.08*responsiveness+0.08*fairness-0.06*uncertainty-0.10*harm, 0.0, 1.0)
}

func main() {
	fmt.Printf("Legitimacy score: %.6f\n", legitimacyScore(0.88, 0.88, 0.88, 0.84, 0.86, 0.88))
	fmt.Printf("Next trust: %.6f\n", nextTrust(0.62, 0.70, 0.78, 0.74, 0.72, 0.36, 0.30))
}
