// public_policy_runner.go
// Run with: go run public_policy_runner.go

package main

import "fmt"

func policyValueScore(efficiency float64, equity float64, resilience float64, feasibility float64, legitimacy float64, implementationCapacity float64) float64 {
	return 0.18*efficiency + 0.22*equity + 0.18*resilience + 0.14*feasibility + 0.14*legitimacy + 0.14*implementationCapacity
}

func requiresReview(equity float64, legitimacy float64, implementationCapacity float64) bool {
	return equity < 0.55 || legitimacy < 0.55 || implementationCapacity < 0.55
}

func main() {
	score := policyValueScore(0.72, 0.84, 0.70, 0.76, 0.80, 0.86)
	fmt.Printf("Policy value score: %.6f\n", score)
	fmt.Printf("Requires review? %t\n", requiresReview(0.46, 0.54, 0.68))
}
